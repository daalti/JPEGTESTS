"""
Configuration Generator Module
Generates UI configurations from JSON files with schema validation
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional, Union, Type, Callable
from dataclasses import dataclass, asdict
import logging
from enum import Enum

# JSON Schema validation
from jsonschema import validate, ValidationError as JsonSchemaError, Draft7Validator

from .state_machine import State, SimpleState, TransitionConfig, StateMachine
from .option_handler import OptionConfig, OptionType, OptionValidator, OptionTransformer
import re


class ConfigError(Exception):
    """Configuration related errors."""
    pass


class ConfigLoader:
    """Loads and validates configuration from files."""
    
    # Schema definitions for validation
    STATE_SCHEMA = {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "type": {"type": "string", "enum": ["simple", "conditional", "timed"]},
            "metadata": {
                "type": "object",
                "properties": {
                    "description": {"type": "string"},
                    "view_elements": {"type": "array", "items": {"type": "string"}},
                    "can_exit_to_home": {"type": "boolean"}
                }
            },
            "entry_condition": {"type": "string"},
            "exit_condition": {"type": "string"},
            "timeout": {"type": "number"},
            "timeout_state": {"type": "string"}
        },
        "required": ["name", "type"]
    }
    
    TRANSITION_SCHEMA = {
        "type": "object",
        "properties": {
            "from_state": {"type": "string"},
            "to_state": {"type": "string"},
            "condition": {"type": "string"},
            "action": {"type": "string"},
            "validators": {
                "type": "array",
                "items": {"type": "string"}
            },
            "metadata": {
                "type": "object",
                "properties": {
                    "button": {"type": "string"},
                    "animation_duration": {"type": "number"},
                    "auto_transition": {"type": "boolean"},
                    "scrolling": {  # Nueva configuración de scrolling
                        "type": "object",
                        "properties": {
                            "required": {"type": "boolean"},
                            "container": {"type": ["string", "null"]},
                            "scrollbar": {"type": ["string", "null"]}, 
                            "direction": {"type": "string", "enum": ["vertical", "horizontal"]},
                            "increment": {"type": "number"}
                        },
                        "required": ["required"]
                    }
                }
            }
        },
        "required": ["from_state", "to_state"]
    }
    
    OPTION_SCHEMA = {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "type": {
                "type": "string",
                "enum": ["combo", "toggle", "spinbox", "radio", "checkbox", "slider", "text", "date", "color"]
            },
            "locator": {
                "oneOf": [
                    {"type": "string"},
                    {"type": "array", "items": {"type": "string"}}
                ]
            },
            "valid_values": {"type": "object"},
            "default_value": {},
            "min_value": {"type": "number"},
            "max_value": {"type": "number"},
            "container_view": {"type": "string"},
            "scrollbar": {"type": "string"},
            "requires_click_to_open": {"type": "boolean"},
            "scroll_increment": {"type": "number"},
            "scroll_direction": {"type": "string", "enum": ["vertical", "horizontal"]},  # New field
            "validators": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "type": {"type": "string"},
                        "params": {"type": "object"}
                    },
                    "required": ["name", "type"]
                }
            },
            "transformers": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "type": {"type": "string"},
                        "params": {"type": "object"}
                    },
                    "required": ["name", "type"]
                }
            },
            "dependencies": {
                "type": "array",
                "items": {"type": "string"}
            },
            "cache_enabled": {"type": "boolean"},
            "cache_ttl": {"type": "number"},
            "description": {"type": "string"},
            "metadata": {"type": "object"}
        },
        "required": ["name", "type", "locator"]
    }
    
    # Fixed WORKFLOW_SCHEMA with proper definitions structure
    WORKFLOW_SCHEMA = {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "version": {"type": "string"},
            "description": {"type": "string"},
            "states": {
                "type": "array",
                "items": {"$ref": "#/definitions/state"}
            },
            "transitions": {
                "type": "array",
                "items": {"$ref": "#/definitions/transition"}
            },
            "options": {
                "type": "array",
                "items": {"$ref": "#/definitions/option"}
            },
            "initial_state": {"type": "string"},
            "metadata": {"type": "object"}
        },
        "required": ["name", "version"],
        "definitions": {
            "state": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "type": {"type": "string", "enum": ["simple", "conditional", "timed"]},
                    "metadata": {
                        "type": "object",
                        "properties": {
                            "description": {"type": "string"},
                            "view_elements": {"type": "array", "items": {"type": "string"}},
                            "can_exit_to_home": {"type": "boolean"}
                        }
                    },
                    "entry_condition": {"type": "string"},
                    "exit_condition": {"type": "string"},
                    "timeout": {"type": "number"},
                    "timeout_state": {"type": "string"}
                },
                "required": ["name", "type"]
            },
            "transition": {
                "type": "object",
                "properties": {
                    "from_state": {"type": "string"},
                    "to_state": {"type": "string"},
                    "condition": {"type": "string"},
                    "action": {"type": "string"},
                    "validators": {
                        "type": "array",
                        "items": {"type": "string"}
                    },
                    "metadata": {"type": "object"}
                },
                "required": ["from_state", "to_state"]
            },
            "option": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "type": {
                        "type": "string",
                        "enum": ["combo", "toggle", "spinbox", "radio", "checkbox", "slider", "text", "date", "color"]
                    },
                    "locator": {
                        "oneOf": [
                            {"type": "string"},
                            {"type": "array", "items": {"type": "string"}}
                        ]
                    },
                    "valid_values": {"type": "object"},
                    "default_value": {},
                    "min_value": {"type": "number"},
                    "max_value": {"type": "number"},
                    "container_view": {"type": "string"},
                    "scrollbar": {"type": "string"},
                    "requires_click_to_open": {"type": "boolean"},
                    "scroll_increment": {"type": "number"},
                    "validators": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "name": {"type": "string"},
                                "type": {"type": "string"},
                                "params": {"type": "object"}
                            },
                            "required": ["name", "type"]
                        }
                    },
                    "transformers": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "name": {"type": "string"},
                                "type": {"type": "string"},
                                "params": {"type": "object"}
                            },
                            "required": ["name", "type"]
                        }
                    },
                    "dependencies": {
                        "type": "array",
                        "items": {"type": "string"}
                    },
                    "cache_enabled": {"type": "boolean"},
                    "cache_ttl": {"type": "number"},
                    "description": {"type": "string"},
                    "metadata": {"type": "object"}
                },
                "required": ["name", "type", "locator"]
            }
        }
    }
    
    def __init__(self, logger: Optional[logging.Logger] = None):
        self._logger = logger or logging.getLogger(__name__)
        self._validators = Draft7Validator(self.WORKFLOW_SCHEMA)
        self._locator_resolver: Optional[LocatorResolver] = None
        
    def set_locator_resolver(self, resolver: 'LocatorResolver') -> None:
        """Set locator resolver for converting string references to actual locators."""
        self._locator_resolver = resolver
    
    def load_from_file(self, file_path: Union[str, Path]) -> Dict[str, Any]:
        """
        Load configuration from JSON file.
        
        Args:
            file_path: Path to JSON configuration file
            
        Returns:
            Loaded configuration dictionary
            
        Raises:
            ConfigError: If file cannot be loaded or is invalid
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise ConfigError(f"Configuration file not found: {file_path}")
        
        try:
            with open(file_path, 'r') as f:
                if file_path.suffix == '.json':
                    config = json.load(f)
                else:
                    raise ConfigError(f"Only JSON files are supported, got: {file_path.suffix}")
            
            self._logger.info(f"Loaded configuration from {file_path}")
            return config
            
        except json.JSONDecodeError as e:
            raise ConfigError(f"Invalid JSON format: {e}")
        except Exception as e:
            raise ConfigError(f"Failed to load configuration: {e}")
    
    def load_hierarchical_config(
        self, 
        base_config_path: Union[str, Path], 
        override_config_path: Union[str, Path]
    ) -> Dict[str, Any]:
        """
        Load configuration with base and override pattern.
        
        Args:
            base_config_path: Path to base/common configuration file
            override_config_path: Path to override/specific configuration file
            
        Returns:
            Merged configuration dictionary
            
        Raises:
            ConfigError: If files cannot be loaded or merged
        """
        # Load base configuration
        base_config = self.load_from_file(base_config_path)
        
        # Load override configuration
        override_config = self.load_from_file(override_config_path)
        
        # Merge configurations
        merged_config = self._deep_merge_configs(base_config, override_config)
        
        self._logger.info(f"Merged configurations: {base_config_path} + {override_config_path}")
        
        return merged_config
    
    def _deep_merge_configs(self, base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
        """
        Deep merge two configuration dictionaries.
        Override values take precedence over base values.
        Arrays are merged by name/key when possible.
        
        Args:
            base: Base configuration dictionary
            override: Override configuration dictionary
            
        Returns:
            Merged configuration dictionary
        """
        result = base.copy()
        
        for key, override_value in override.items():
            if key not in result:
                # New key from override
                result[key] = override_value
            elif isinstance(override_value, dict) and isinstance(result[key], dict):
                # Recursive merge for nested dictionaries
                result[key] = self._deep_merge_configs(result[key], override_value)
            elif isinstance(override_value, list) and isinstance(result[key], list):
                # Special handling for arrays based on content type
                result[key] = self._merge_arrays(result[key], override_value, key)
            else:
                # Simple override
                result[key] = override_value
        
        return result
    
    def _merge_arrays(self, base_array: List[Any], override_array: List[Any], array_key: str) -> List[Any]:
        """
        Merge arrays based on their content and context.
        
        Args:
            base_array: Base array
            override_array: Override array  
            array_key: Key name to determine merge strategy
            
        Returns:
            Merged array
        """
        # Special handling for states, transitions, and options
        if array_key in ["states", "transitions", "options"]:
            return self._merge_named_objects(base_array, override_array, array_key)
        else:
            # For other arrays, override completely
            return override_array
    
    def _merge_named_objects(self, base_objects: List[Dict], override_objects: List[Dict], object_type: str) -> List[Dict]:
        """
        Merge arrays of named objects (states, transitions, options).
        Objects are matched by name/key and merged or replaced.
        
        Args:
            base_objects: Base array of objects
            override_objects: Override array of objects
            object_type: Type of objects being merged
            
        Returns:
            Merged array of objects
        """
        # Get the key used to identify objects
        id_key = self._get_object_id_key(object_type)
        
        # Create lookup maps
        base_map = {obj.get(id_key): obj for obj in base_objects if id_key in obj}
        override_map = {obj.get(id_key): obj for obj in override_objects if id_key in obj}
        
        # Merge objects
        result = []
        
        # Process base objects
        for obj_id, base_obj in base_map.items():
            if obj_id in override_map:
                # Merge with override
                if object_type == "transitions":
                    # For transitions, use composite key
                    merged_obj = self._deep_merge_configs(base_obj, override_map[obj_id])
                else:
                    # For states and options, merge normally
                    merged_obj = self._deep_merge_configs(base_obj, override_map[obj_id])
                result.append(merged_obj)
            else:
                # Keep base object as-is
                result.append(base_obj)
        
        # Add new objects from override
        for obj_id, override_obj in override_map.items():
            if obj_id not in base_map:
                result.append(override_obj)
        
        # Handle transitions specially (they have composite keys)
        if object_type == "transitions":
            result = self._merge_transitions_by_composite_key(base_objects, override_objects)
        
        return result
    
    def _merge_transitions_by_composite_key(self, base_transitions: List[Dict], override_transitions: List[Dict]) -> List[Dict]:
        """
        Merge transitions using composite key (from_state + to_state).
        
        Args:
            base_transitions: Base transitions
            override_transitions: Override transitions
            
        Returns:
            Merged transitions
        """
        # Create composite keys for transitions
        base_map = {}
        for trans in base_transitions:
            key = f"{trans.get('from_state')}:{trans.get('to_state')}"
            base_map[key] = trans
        
        override_map = {}
        for trans in override_transitions:
            key = f"{trans.get('from_state')}:{trans.get('to_state')}"
            override_map[key] = trans
        
        # Merge
        result = []
        
        # Process base transitions
        for key, base_trans in base_map.items():
            if key in override_map:
                # Merge with override
                merged_trans = self._deep_merge_configs(base_trans, override_map[key])
                result.append(merged_trans)
            else:
                # Keep base transition
                result.append(base_trans)
        
        # Add new transitions from override
        for key, override_trans in override_map.items():
            if key not in base_map:
                result.append(override_trans)
        
        return result
    
    def _get_object_id_key(self, object_type: str) -> str:
        """Get the key used to identify objects of given type."""
        type_keys = {
            "states": "name",
            "options": "name",
            "transitions": "from_state"  # Special case, handled separately
        }
        return type_keys.get(object_type, "name")
    
    def validate_config(self, config: Dict[str, Any]) -> None:
        """
        Validate configuration against schema.
        
        Args:
            config: Configuration dictionary to validate
            
        Raises:
            ConfigError: If configuration is invalid
        """
        try:
            self._validators.validate(config)
            self._logger.info("Configuration validation successful")
        except JsonSchemaError as e:
            raise ConfigError(f"Configuration validation failed: {e.message}")
    
    def load_and_validate(self, file_path: Union[str, Path]) -> Dict[str, Any]:
        """
        Load and validate configuration from file.
        
        Args:
            file_path: Path to configuration file
            
        Returns:
            Validated configuration dictionary
        """
        config = self.load_from_file(file_path)
        self.validate_config(config)
        return config


class LocatorResolver:
    """Resolves string locator references to actual locator objects."""
    
    def __init__(self, locator_module: Any):
        """
        Initialize with locator module containing locator definitions.
        
        Args:
            locator_module: Module containing locator constants (e.g., CopyLoc)
        """
        self._locator_module = locator_module
        self._cache: Dict[str, Any] = {}
    
    def resolve(self, locator_ref: Union[str, List[str]]) -> Any:
        """
        Resolve locator reference to actual locator object.
        
        Args:
            locator_ref: String reference or list of references
            
        Returns:
            Resolved locator object
        """
        if isinstance(locator_ref, list):
            return [self._resolve_single(ref) for ref in locator_ref]
        return self._resolve_single(locator_ref)
    
    def _resolve_single(self, ref: str) -> Any:
        """Resolve single locator reference."""
        if ref in self._cache:
            return self._cache[ref]
        
        # Parse reference (e.g., "CopyLoc.button_start")
        parts = ref.split('.')
        
        obj = self._locator_module
        for part in parts:
            if hasattr(obj, part):
                obj = getattr(obj, part)
            else:
                raise ConfigError(f"Cannot resolve locator reference: {ref}")
        
        self._cache[ref] = obj
        return obj


class ValidatorFactory:
    """Factory for creating validators from configuration."""
    
    VALIDATOR_TYPES = {
        "range": lambda params: OptionValidator(
            name=params.get("name", "range"),
            validator=lambda v: params["min"] <= v <= params["max"],
            error_message=f"Value must be between {params['min']} and {params['max']}"
        ),
        "regex": lambda params: OptionValidator(
            name=params.get("name", "regex"),
            validator=lambda v: bool(re.match(params["pattern"], str(v))),
            error_message=f"Value must match pattern {params['pattern']}"
        ),
        "length": lambda params: OptionValidator(
            name=params.get("name", "length"),
            validator=lambda v: params.get("min", 0) <= len(str(v)) <= params.get("max", float('inf')),
            error_message=f"Length must be between {params.get('min', 0)} and {params.get('max', 'unlimited')}"
        ),
        "enum": lambda params: OptionValidator(
            name=params.get("name", "enum"),
            validator=lambda v: v in params["values"],
            error_message=f"Value must be one of {params['values']}"
        ),
        "custom": lambda params: OptionValidator(
            name=params.get("name", "custom"),
            validator=eval(params["function"]),  # Note: Be careful with eval in production
            error_message=params.get("error_message", "Custom validation failed")
        )
    }
    
    @classmethod
    def create(cls, validator_config: Dict[str, Any]) -> OptionValidator:
        """Create validator from configuration."""
        validator_type = validator_config["type"]
        
        if validator_type not in cls.VALIDATOR_TYPES:
            raise ConfigError(f"Unknown validator type: {validator_type}")
        
        return cls.VALIDATOR_TYPES[validator_type](validator_config.get("params", {}))


class TransformerFactory:
    """Factory for creating transformers from configuration."""
    
    TRANSFORMER_TYPES = {
        "uppercase": lambda params: OptionTransformer(
            name=params.get("name", "uppercase"),
            transformer=lambda v: str(v).upper()
        ),
        "lowercase": lambda params: OptionTransformer(
            name=params.get("name", "lowercase"),
            transformer=lambda v: str(v).lower()
        ),
        "strip": lambda params: OptionTransformer(
            name=params.get("name", "strip"),
            transformer=lambda v: str(v).strip()
        ),
        "round": lambda params: OptionTransformer(
            name=params.get("name", "round"),
            transformer=lambda v: round(float(v), params.get("decimals", 0))
        ),
        "multiply": lambda params: OptionTransformer(
            name=params.get("name", "multiply"),
            transformer=lambda v: float(v) * params["factor"]
        ),
        "custom": lambda params: OptionTransformer(
            name=params.get("name", "custom"),
            transformer=eval(params["function"])  # Note: Be careful with eval
        )
    }
    
    @classmethod
    def create(cls, transformer_config: Dict[str, Any]) -> OptionTransformer:
        """Create transformer from configuration."""
        transformer_type = transformer_config["type"]
        
        if transformer_type not in cls.TRANSFORMER_TYPES:
            raise ConfigError(f"Unknown transformer type: {transformer_type}")
        
        return cls.TRANSFORMER_TYPES[transformer_type](transformer_config.get("params", {}))


class ConfigGenerator:
    """Generates UI operation configurations from JSON files."""
    
    def __init__(
        self,
        config_file: Union[str, Path],
        base_config_file: Optional[Union[str, Path]] = None,
        locator_module: Optional[Any] = None,
        logger: Optional[logging.Logger] = None,
        feature_name: Optional[str] = None
    ):
        """
        Initialize ConfigGenerator with optional base configuration.
        
        Args:
            config_file: Main configuration file path
            base_config_file: Optional base configuration file path
            locator_module: Module containing locator definitions
            logger: Logger instance
        """
        self._logger = logger or logging.getLogger(__name__)
        self._loader = ConfigLoader(logger)
        self._feature_name = feature_name
        
        if locator_module:
            self._locator_resolver = LocatorResolver(locator_module)
            self._loader.set_locator_resolver(self._locator_resolver)
        else:
            self._locator_resolver = None
        
        if not base_config_file:
            raise ConfigError("Base configuration file must be provided for hierarchical loading.")
        
        # Load configuration (hierarchical or single file)
        if config_file:
            self._config = self._loader.load_hierarchical_config(base_config_file, config_file)
            self._logger.info(f"Loaded hierarchical configuration: {base_config_file} + {config_file}")
        else:
            self._config = self._loader.load_and_validate(base_config_file)
            self._logger.info(f"Loaded single configuration: {base_config_file}")
        
        # Validate final merged configuration
        self._loader.validate_config(self._config)
        
        # Generated objects
        self._states: Dict[str, State] = {}
        self._transitions: List[TransitionConfig] = []
        self._options: Dict[str, OptionConfig] = {}
        
        # Generate configurations
        self._generate_all()

    def get_feature_name(self) -> Optional[str]:
        """Get the feature name this configuration belongs to."""
        return self._feature_name
    
    def get_home_capable_states(self) -> List[str]:
        """Get list of states that can exit to home."""
        home_states = []
        for state_name, state in self._states.items():
            if state.metadata.get("can_exit_to_home"):
                home_states.append(state_name)
        return home_states
    
    @classmethod
    def from_size_config(
        cls,
        size: str,
        feature: str,
        type: str,
        config_dir: Union[str, Path],
        locator_module: Optional[Any] = None,
        logger: Optional[logging.Logger] = None
    ) -> "ConfigGenerator":
        """
        Create ConfigGenerator for specific size with common base.
        
        Args:
            size: Size identifier (xl, l, m, s, xs)
            feature: Feature identifier (e.g., "copy")
            type: Type identifier (e.g., "workflow")
            config_dir: Directory containing configuration files
            locator_module: Module containing locator definitions
            logger: Logger instance
            
        Returns:
            Configured ConfigGenerator instance
        """
        config_dir = Path(config_dir)
        
        # Common configuration file
        base_config_file = config_dir / f"{feature}_{type}_common.json"
        
        # Size-specific configuration file
        size_config_file = config_dir / f"{feature}_{type}_{size}.json"
        
        if not base_config_file.exists():
            raise ConfigError(f"Common configuration file not found: {base_config_file}")
        
        if not size_config_file.exists():
            raise ConfigError(f"Size-specific configuration file not found: {size_config_file}")
        
        return cls(
            config_file=size_config_file,
            base_config_file=base_config_file,
            locator_module=locator_module,
            logger=logger
        )
    
    def _generate_all(self) -> None:
        """Generate all configurations from loaded data."""
        self._generate_states()
        self._generate_transitions()
        self._generate_options()
    
    def _generate_states(self) -> None:
        """Generate state objects from configuration."""
        for state_config in self._config.get("states", []):
            state = self._create_state(state_config)
            self._states[state.name] = state
            self._logger.debug(f"Generated state: {state.name}")
    
    def _create_state(self, config: Dict[str, Any]) -> State:
        """Create state object from configuration."""
        state_type = config.get("type", "simple")
        
        if state_type == "simple":
            return SimpleState(
                name=config["name"],
                metadata=config.get("metadata", {})
            )
        # Add more state types as needed
        else:
            raise ConfigError(f"Unknown state type: {state_type}")
    
    def _generate_transitions(self) -> None:
        """Generate transition configurations."""
        for trans_config in self._config.get("transitions", []):
            transition = TransitionConfig(
                from_state=trans_config["from_state"],
                to_state=trans_config["to_state"],
                condition=self._create_condition(trans_config.get("condition")),
                action=self._create_action(trans_config.get("action")),
                validators=[self._create_condition(v) for v in trans_config.get("validators", [])], #type: ignore
                metadata=trans_config.get("metadata", {})
            )
            self._transitions.append(transition)
            self._logger.debug(f"Generated transition: {transition.from_state} -> {transition.to_state}")
    
    def _generate_options(self) -> None:
        """Generate option configurations."""
        for opt_config in self._config.get("options", []):
            option = self._create_option(opt_config)
            self._options[option.name] = option
            self._logger.debug(f"Generated option: {option.name}")
    
    def _create_option(self, config: Dict[str, Any]) -> OptionConfig:
        """Create option configuration from data."""
        # Resolve locators
        locator = config["locator"]
        if self._locator_resolver:
            if isinstance(locator, str):
                locator = self._locator_resolver.resolve(locator)
            elif isinstance(locator, list):
                locator = [self._locator_resolver.resolve(loc) for loc in locator]
        
        # Create validators
        validators = [
            ValidatorFactory.create(v)
            for v in config.get("validators", [])
        ]
        
        # Create transformers
        transformers = [
            TransformerFactory.create(t)
            for t in config.get("transformers", [])
        ]
        
        return OptionConfig(
            name=config["name"],
            option_type=OptionType(config["type"]),
            locator=locator,
            valid_values=config.get("valid_values"),
            default_value=config.get("default_value"),
            min_value=config.get("min_value"),
            max_value=config.get("max_value"),
            container_view=self._resolve_locator(config.get("container_view")),
            scrollbar=self._resolve_locator(config.get("scrollbar")),
            requires_click_to_open=config.get("requires_click_to_open", False),
            scroll_increment=config.get("scroll_increment", 0.1),
            scroll_direction=config.get("scroll_direction", "vertical"),  # New field with default
            validators=validators,
            transformers=transformers,
            dependencies=config.get("dependencies", []),
            cache_enabled=config.get("cache_enabled", True),
            cache_ttl=config.get("cache_ttl", 60.0),
            description=config.get("description", ""),
            metadata=config.get("metadata", {})
        )
    
    def _resolve_locator(self, locator_ref: Optional[str]) -> Optional[Any]:
        """Resolve optional locator reference."""
        if locator_ref and self._locator_resolver:
            return self._locator_resolver.resolve(locator_ref)
        return locator_ref
    
    def _create_condition(self, condition_str: Optional[str]) -> Optional[Callable]:
        """Create condition function from string."""
        if not condition_str:
            return None
        
        # Simple implementation - in production, use safer evaluation
        return lambda context: eval(condition_str, {"context": context})
    
    def _create_action(self, action_str: Optional[str]) -> Optional[Callable]:
        """Create action function from string."""
        if not action_str:
            return None
        
        # Simple implementation - in production, use safer evaluation
        return lambda context: exec(action_str, {"context": context})
    
    def get_state_machine(self) -> StateMachine:
        """Create and configure state machine from generated configurations."""
        machine = StateMachine(
            initial_state=self._config.get("initial_state"),
            logger=self._logger
        )
        
        # Register states
        for state in self._states.values():
            machine.register_state(state)
        
        # Register transitions
        for transition in self._transitions:
            machine.register_transition(transition)
        
        return machine
    
    def get_options(self) -> Dict[str, OptionConfig]:
        """Get generated option configurations."""
        return self._options.copy()
    
    def get_metadata(self) -> Dict[str, Any]:
        """Get workflow metadata."""
        return {
            "name": self._config.get("name"),
            "version": self._config.get("version"),
            "description": self._config.get("description"),
            "metadata": self._config.get("metadata", {})
        }
    
    def export_documentation(self, output_path: Optional[Path] = None) -> str:
        """
        Generate documentation from configuration.
        
        Args:
            output_path: Optional path to save documentation
            
        Returns:
            Generated documentation as string
        """
        doc = []
        
        # Header
        doc.append(f"# {self._config.get('name', 'Workflow')} Documentation")
        doc.append(f"Version: {self._config.get('version', '1.0')}")
        doc.append(f"\n{self._config.get('description', '')}\n")
        
        # States
        doc.append("## States\n")
        for state_name, state in sorted(self._states.items()):
            doc.append(f"### {state_name}")
            if state.metadata:
                doc.append(f"Metadata: {state.metadata}")
            doc.append("")
        
        # Transitions
        doc.append("## State Transitions\n")
        doc.append("| From | To | Condition |")
        doc.append("|------|-----|-----------|")
        for trans in self._transitions:
            condition = "Always" if not trans.condition else "Conditional"
            doc.append(f"| {trans.from_state} | {trans.to_state} | {condition} |")
        doc.append("")
        
        # Options
        doc.append("## Options\n")
        for opt_name, opt in sorted(self._options.items()):
            doc.append(f"### {opt_name}")
            doc.append(f"- **Type**: {opt.option_type.value}")
            doc.append(f"- **Description**: {opt.description}")
            
            if opt.valid_values:
                doc.append(f"- **Valid Values**: {list(opt.valid_values.keys())}")
            if opt.default_value is not None:
                doc.append(f"- **Default**: {opt.default_value}")
            if opt.min_value is not None or opt.max_value is not None:
                doc.append(f"- **Range**: {opt.min_value} to {opt.max_value}")
            if opt.dependencies:
                doc.append(f"- **Dependencies**: {opt.dependencies}")
            
            doc.append("")
        
        documentation = "\n".join(doc)
        
        if output_path:
            output_path = Path(output_path)
            output_path.write_text(documentation)
            self._logger.info(f"Documentation saved to {output_path}")
        
        return documentation