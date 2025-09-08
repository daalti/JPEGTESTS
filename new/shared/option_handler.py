"""
Generic Option Handler Module
Reusable option selection and management for UI operations
"""

from typing import Any, Dict, List, Optional, Callable, Union, Tuple
from dataclasses import dataclass, field
from enum import Enum
from abc import ABC, abstractmethod
import logging
import time
from functools import lru_cache


class OptionType(Enum):
    """Types of UI options."""
    COMBO = "combo"
    TOGGLE = "toggle"
    SPINBOX = "spinbox"
    RADIO = "radio"
    CHECKBOX = "checkbox"
    SLIDER = "slider"
    TEXT = "text"
    DATE = "date"
    COLOR = "color"


class ValidationError(Exception):
    """Exception raised when option validation fails."""
    pass


@dataclass
class OptionValidator:
    """Validator for option values."""
    name: str
    validator: Callable[[Any], bool]
    error_message: str = "Validation failed"
    
    def validate(self, value: Any) -> None:
        """
        Validate a value.
        
        Raises:
            ValidationError: If validation fails
        """
        if not self.validator(value):
            raise ValidationError(f"{self.name}: {self.error_message} for value '{value}'")


@dataclass
class OptionTransformer:
    """Transformer for option values."""
    name: str
    transformer: Callable[[Any], Any]
    
    def transform(self, value: Any) -> Any:
        """Transform a value."""
        return self.transformer(value)


@dataclass
class OptionConfig:
    """Configuration for a UI option."""
    # Basic properties
    name: str
    option_type: OptionType
    locator: Union[Any, List[Any]]
    
    # Value configuration
    valid_values: Optional[Dict[str, Any]] = None
    default_value: Optional[Any] = None
    min_value: Optional[Any] = None
    max_value: Optional[Any] = None
    
    # UI interaction
    container_view: Optional[Any] = None
    scrollbar: Optional[Any] = None
    requires_click_to_open: bool = False
    scroll_increment: float = 0.1
    
    # Validation and transformation
    validators: List[OptionValidator] = field(default_factory=list)
    transformers: List[OptionTransformer] = field(default_factory=list)
    
    # Dependencies and conditions
    dependencies: List[str] = field(default_factory=list)
    enabled_condition: Optional[Callable[[], bool]] = None
    visible_condition: Optional[Callable[[], bool]] = None
    
    # Caching
    cache_enabled: bool = True
    cache_ttl: float = 60.0
    
    # Metadata
    description: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def validate(self, value: Any) -> None:
        """Validate a value against all validators."""
        for validator in self.validators:
            validator.validate(value)
    
    def transform(self, value: Any) -> Any:
        """Apply all transformers to a value."""
        for transformer in self.transformers:
            value = transformer.transform(value)
        return value
    
    def is_enabled(self) -> bool:
        """Check if option is enabled."""
        if self.enabled_condition:
            return self.enabled_condition()
        return True
    
    def is_visible(self) -> bool:
        """Check if option is visible."""
        if self.visible_condition:
            return self.visible_condition()
        return True


class OptionHandler(ABC):
    """Abstract base class for option handlers."""
    
    @abstractmethod
    def select_option(self, config: OptionConfig, value: Any) -> None:
        """Select an option value."""
        pass
    
    @abstractmethod
    def get_current_value(self, config: OptionConfig) -> Any:
        """Get current value of an option."""
        pass
    
    @abstractmethod
    def is_available(self, config: OptionConfig) -> bool:
        """Check if option is available in UI."""
        pass


class GenericOptionHandler(OptionHandler):
    """Generic implementation of option handler."""
    
    def __init__(self, driver: Any, logger: Optional[logging.Logger] = None):
        self._driver = driver
        self._logger = logger or logging.getLogger(__name__)
        self._cache: Dict[str, Any] = {}
        self._cache_timestamps: Dict[str, float] = {}
        self._selection_history: List[Dict[str, Any]] = []
        
    def select_option(self, config: OptionConfig, value: Any) -> None:
        """
        Select an option value based on configuration.
        
        Args:
            config: Option configuration
            value: Value to select
            
        Raises:
            ValidationError: If value is invalid
            RuntimeError: If selection fails
        """
        # Check if option is available
        if not config.is_enabled():
            raise RuntimeError(f"Option '{config.name}' is not enabled")
        
        if not config.is_visible():
            raise RuntimeError(f"Option '{config.name}' is not visible")
        
        # Transform value
        value = config.transform(value)
        
        # Validate value
        config.validate(value)
        
        # Log selection attempt
        self._logger.info(f"Selecting {config.name}: {value}")
        
        # Store current value for rollback
        current_value = None
        try:
            current_value = self.get_current_value(config)
        except Exception:
            pass  # Couldn't get current value
        
        # Perform selection based on type
        try:
            if config.option_type == OptionType.COMBO:
                self._select_combo_option(config, value)
            elif config.option_type == OptionType.TOGGLE:
                self._select_toggle_option(config, value)
            elif config.option_type == OptionType.SPINBOX:
                self._select_spinbox_option(config, value)
            elif config.option_type == OptionType.RADIO:
                self._select_radio_option(config, value)
            elif config.option_type == OptionType.CHECKBOX:
                self._select_checkbox_option(config, value)
            elif config.option_type == OptionType.SLIDER:
                self._select_slider_option(config, value)
            elif config.option_type == OptionType.TEXT:
                self._select_text_option(config, value)
            else:
                raise ValueError(f"Unsupported option type: {config.option_type}")
            
            # Update cache
            if config.cache_enabled:
                self._update_cache(config.name, value)
            
            # Record in history
            self._record_selection(config.name, value, current_value)
            
            self._logger.info(f"Successfully selected {config.name}: {value}")
            
        except Exception as e:
            self._logger.error(f"Failed to select {config.name}: {e}")
            # Attempt rollback if we have previous value
            if current_value is not None:
                try:
                    self._logger.info(f"Attempting rollback to {current_value}")
                    self.select_option(config, current_value)
                except Exception:
                    pass  # Rollback failed
            raise
    
    def get_current_value(self, config: OptionConfig) -> Any:
        """Get current value of an option."""
        # Check cache first
        if config.cache_enabled:
            cached_value = self._get_cached_value(config.name, config.cache_ttl)
            if cached_value is not None:
                return cached_value
        
        # Get from UI
        element = self._get_element(config.locator)
        
        if config.option_type == OptionType.TOGGLE:
            value = element.get("checked", False)
        elif config.option_type == OptionType.SPINBOX:
            value = element.get("value", 0)
        elif config.option_type == OptionType.TEXT:
            value = element.get("text", "")
        elif config.option_type == OptionType.SLIDER:
            value = element.get("value", config.min_value or 0)
        else:
            # For combo/radio, need to find selected item
            value = self._get_selected_item(config)
        
        # Update cache
        if config.cache_enabled:
            self._update_cache(config.name, value)
        
        return value
    
    def is_available(self, config: OptionConfig) -> bool:
        """Check if option is available in UI."""
        try:
            element = self._get_element(config.locator)
            return element is not None and element.get("visible", False)
        except Exception:
            return False
    
    def get_selection_history(self, option_name: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get selection history for an option or all options."""
        if option_name:
            return [h for h in self._selection_history if h["option"] == option_name]
        return self._selection_history.copy()
    
    def clear_cache(self, option_name: Optional[str] = None) -> None:
        """Clear cache for an option or all options."""
        if option_name:
            self._cache.pop(option_name, None)
            self._cache_timestamps.pop(option_name, None)
        else:
            self._cache.clear()
            self._cache_timestamps.clear()
    
    # Private methods for specific option types
    
    def _select_combo_option(self, config: OptionConfig, value: str) -> None:
        """Handle combo box selection."""
        if config.valid_values and value not in config.valid_values:
            raise ValidationError(f"Invalid value '{value}' for combo box '{config.name}'")
        
        # Open combo if needed
        if config.requires_click_to_open:
            self._click_element(config.locator)
            time.sleep(0.5)  # Wait for dropdown
        
        # Wait for container
        if config.container_view:
            self._wait_for_element(config.container_view)
        
        # Select value
        if config.valid_values:
            value_locator = config.valid_values[value]
            
            if config.scrollbar:
                self._scroll_to_element(value_locator, config.scrollbar, config.scroll_increment)
            
            self._click_element(value_locator)
        else:
            # Direct selection
            self._set_element_value(config.locator, value)
    
    def _select_toggle_option(self, config: OptionConfig, value: bool) -> None:
        """Handle toggle selection."""
        element = self._get_element(config.locator)
        current_state = element.get("checked", False)
        
        if current_state != value:
            self._click_element(config.locator)
    
    def _select_spinbox_option(self, config: OptionConfig, value: Union[int, float]) -> None:
        """Handle spinbox selection."""
        # Validate range
        if config.min_value is not None and value < config.min_value:
            raise ValidationError(f"Value {value} below minimum {config.min_value}")
        if config.max_value is not None and value > config.max_value:
            raise ValidationError(f"Value {value} above maximum {config.max_value}")
        
        self._set_element_value(config.locator, value)
    
    def _select_radio_option(self, config: OptionConfig, value: str) -> None:
        """Handle radio button selection."""
        if config.valid_values and value in config.valid_values:
            self._click_element(config.valid_values[value])
        else:
            raise ValidationError(f"Invalid radio option '{value}'")
    
    def _select_checkbox_option(self, config: OptionConfig, values: List[str]) -> None:
        """Handle checkbox selection (multiple values)."""
        if not config.valid_values:
            raise ValidationError("No valid values defined for checkboxes")
        
        # Uncheck all first
        for checkbox_value, locator in config.valid_values.items():
            element = self._get_element(locator)
            if element.get("checked", False):
                self._click_element(locator)
        
        # Check selected values
        for value in values:
            if value in config.valid_values:
                self._click_element(config.valid_values[value])
            else:
                raise ValidationError(f"Invalid checkbox value '{value}'")
    
    def _select_slider_option(self, config: OptionConfig, value: Union[int, float]) -> None:
        """Handle slider selection."""
        # Validate range
        if config.min_value is not None and value < config.min_value:
            raise ValidationError(f"Value {value} below minimum {config.min_value}")
        if config.max_value is not None and value > config.max_value:
            raise ValidationError(f"Value {value} above maximum {config.max_value}")
        
        # Set slider value
        self._set_element_value(config.locator, value)
    
    def _select_text_option(self, config: OptionConfig, value: str) -> None:
        """Handle text input."""
        # Clear and type
        element = self._get_element(config.locator)
        self._clear_element(config.locator)
        self._type_text(config.locator, value)
    
    # Helper methods
    
    def _get_element(self, locator: Union[Any, List[Any]]) -> Any:
        """Get element from driver."""
        if isinstance(locator, list):
            # Nested locators
            return self._driver.find_nested_element(locator)
        return self._driver.find(locator)
    
    def _wait_for_element(self, locator: Any, timeout: float = 10.0) -> Any:
        """Wait for element to be available."""
        return self._driver.wait_for(
            locator,
            condition=lambda el: el.get("visible", False),
            timeout=timeout
        )
    
    def _click_element(self, locator: Any) -> None:
        """Click an element."""
        element = self._get_element(locator)
        self._driver.click(element)
    
    def _set_element_value(self, locator: Any, value: Any) -> None:
        """Set element value."""
        element = self._get_element(locator)
        element["value"] = value
    
    def _clear_element(self, locator: Any) -> None:
        """Clear element content."""
        element = self._get_element(locator)
        element["value"] = ""
    
    def _type_text(self, locator: Any, text: str) -> None:
        """Type text into element."""
        element = self._get_element(locator)
        self._driver.type_text(element, text)
    
    def _scroll_to_element(self, locator: Any, scrollbar: Any, increment: float) -> None:
        """Scroll to make element visible."""
        self._driver.scroll_to_element(locator, scrollbar, increment)
    
    def _get_selected_item(self, config: OptionConfig) -> Any:
        """Get currently selected item in combo/radio."""
        # Implementation depends on UI framework
        return None
    
    # Cache management
    
    def _get_cached_value(self, key: str, ttl: float) -> Optional[Any]:
        """Get cached value if not expired."""
        if key not in self._cache:
            return None
        
        timestamp = self._cache_timestamps.get(key, 0)
        if time.time() - timestamp > ttl:
            # Expired
            del self._cache[key]
            del self._cache_timestamps[key]
            return None
        
        return self._cache[key]
    
    def _update_cache(self, key: str, value: Any) -> None:
        """Update cache with new value."""
        self._cache[key] = value
        self._cache_timestamps[key] = time.time()
    
    def _record_selection(self, option_name: str, new_value: Any, old_value: Any) -> None:
        """Record selection in history."""
        self._selection_history.append({
            "option": option_name,
            "new_value": new_value,
            "old_value": old_value,
            "timestamp": time.time()
        })
        
        # Limit history size
        if len(self._selection_history) > 1000:
            self._selection_history = self._selection_history[-500:]


class BatchOptionHandler(GenericOptionHandler):
    """Handler for batch option operations."""
    
    def select_multiple(self, selections: List[Tuple[OptionConfig, Any]]) -> List[bool]:
        """
        Select multiple options in batch.
        
        Args:
            selections: List of (config, value) tuples
            
        Returns:
            List of success flags for each selection
        """
        results = []
        
        for config, value in selections:
            try:
                self.select_option(config, value)
                results.append(True)
            except Exception as e:
                self._logger.error(f"Batch selection failed for {config.name}: {e}")
                results.append(False)
        
        return results
    
    def reset_to_defaults(self, configs: List[OptionConfig]) -> None:
        """Reset options to their default values."""
        for config in configs:
            if config.default_value is not None:
                try:
                    self.select_option(config, config.default_value)
                except Exception as e:
                    self._logger.error(f"Failed to reset {config.name} to default: {e}")