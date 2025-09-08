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
            "metadata": {"type": "object"},
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
            "metadata": {"type": "object"}
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
                    "metadata": {"type": "object"},
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
        locator_module: Optional[Any] = None,
        logger: Optional[logging.Logger] = None
    ):
        self._logger = logger or logging.getLogger(__name__)
        self._loader = ConfigLoader(logger)
        
        if locator_module:
            self._locator_resolver = LocatorResolver(locator_module)
            self._loader.set_locator_resolver(self._locator_resolver)
        else:
            self._locator_resolver = None
        
        # Load and validate configuration
        self._config = self._loader.load_and_validate(config_file)
        
        # Generated objects
        self._states: Dict[str, State] = {}
        self._transitions: List[TransitionConfig] = []
        self._options: Dict[str, OptionConfig] = {}
        
        # Generate configurations
        self._generate_all()
    
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
        if self._locator_resolver and isinstance(locator, str):
            locator = self._locator_resolver.resolve(locator)
        
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