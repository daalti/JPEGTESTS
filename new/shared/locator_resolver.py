"""
Centralized Locator Resolution Module
Simplifies locator handling across the entire UI testing framework
"""

from typing import Union, List, Any, Optional
import logging
from dunetuf.ui.new.shared.locator_base import Locator

# Type alias for cleaner code
LocatorInput = Union[str, Locator, List[Union[str, Locator]]]

class LocatorResolver:
    """Centralized locator resolution with fallback strategies."""
    
    def __init__(self, locator_provider: Any = None, config_generator: Any = None):
        self._locator_provider = locator_provider
        self._config_generator = config_generator
        self._logger = logging.getLogger(__name__)
    
    def resolve(self, locator_input: LocatorInput) -> Union[Locator, str, List[Union[Locator, str]]]:
        """
        Universal locator resolver with multiple strategies.
        
        Args:
            locator_input: String reference, Locator object, or list of either
            
        Returns:
            Resolved locator(s) ready for driver use
        """
        if isinstance(locator_input, list):
            return [self._resolve_single(item) for item in locator_input]
        
        return self._resolve_single(locator_input)
    
    def _resolve_single(self, locator_input: Union[str, Locator]) -> Union[Locator, str]:
        """Resolve a single locator input."""
        
        # Strategy 1: Already a Locator object
        if isinstance(locator_input, Locator):
            return locator_input
        
        # Strategy 2: Direct CSS selector string
        if isinstance(locator_input, str) and locator_input.startswith(('#', '.', '[')):
            return locator_input
        
        # Strategy 3: Config generator resolution (if available)
        if (isinstance(locator_input, str) and 
            self._config_generator and 
            hasattr(self._config_generator, '_locator_resolver') and 
            self._config_generator._locator_resolver):
            
            try:
                return self._config_generator._locator_resolver.resolve(locator_input)
            except Exception as e:
                self._logger.debug(f"Config generator resolution failed for '{locator_input}': {e}")
        
        # Strategy 4: Locator provider attribute lookup
        if isinstance(locator_input, str) and self._locator_provider:
            try:
                return getattr(self._locator_provider, locator_input)
            except AttributeError:
                self._logger.debug(f"Locator '{locator_input}' not found in provider")
        
        # Strategy 5: Fallback - assume it's a CSS selector
        if isinstance(locator_input, str):
            self._logger.warning(f"Using fallback CSS resolution for: {locator_input}")
            return f"#{locator_input}" if not locator_input.startswith(('#', '.', '[')) else locator_input
        
        # Final fallback
        raise ValueError(f"Cannot resolve locator input: {locator_input}")
    
    def resolve_to_selector_string(self, locator_input: LocatorInput) -> Union[str, List[str]]:
        """
        Resolve locator input to CSS selector string(s).
        
        Args:
            locator_input: Any valid locator input
            
        Returns:
            CSS selector string(s) ready for driver._normalize_selector
        """
        resolved = self.resolve(locator_input)
        
        if isinstance(resolved, list):
            return [self._to_selector_string(item) for item in resolved]
        
        return self._to_selector_string(resolved)
    
    def _to_selector_string(self, locator: Union[Locator, str]) -> str:
        """Convert resolved locator to CSS selector string."""
        if isinstance(locator, str):
            return locator
        
        if isinstance(locator, Locator):
            if locator.how != "css":
                raise ValueError(f"Unsupported locator strategy: {locator.how}")
            return locator.what
        
        raise ValueError(f"Cannot convert to selector string: {locator}")

# Global resolver instance for easy access
_global_resolver: Optional[LocatorResolver] = None

def get_resolver() -> LocatorResolver:
    """Get global resolver instance."""
    global _global_resolver
    if _global_resolver is None:
        _global_resolver = LocatorResolver()
    return _global_resolver

def set_resolver(resolver: LocatorResolver) -> None:
    """Set global resolver instance."""
    global _global_resolver
    _global_resolver = resolver

def resolve_locator(locator_input: LocatorInput) -> Union[Locator, str, List[Union[Locator, str]]]:
    """Convenience function for quick resolution."""
    return get_resolver().resolve(locator_input)

def resolve_to_selector(locator_input: LocatorInput) -> Union[str, List[str]]:
    """Convenience function for selector string resolution."""
    return get_resolver().resolve_to_selector_string(locator_input)