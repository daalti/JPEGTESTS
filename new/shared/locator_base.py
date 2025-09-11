from dataclasses import dataclass
from typing import Literal, Final, Callable, Union

Strategy = Literal["css", "xpath", "object_id", "aria", "testid"]

@dataclass(frozen=True)
class Locator:
    how: Strategy
    what: str

# Helpers cortos
def CSS(q: str) -> Locator: return Locator("css", q)
def OID(q: str) -> Locator: return Locator("object_id", q)

class LocatorCombiner:
    """Utility class to combine CSS locators."""
    
    @staticmethod
    def combine(*locators: Union[Locator, str], separator: str = " ") -> Locator:
        """
        Combine multiple locators into a single CSS selector.
        
        Args:
            *locators: Locators or strings to combine
            separator: Separator between selectors (default: " " for descendant)
        
        Returns:
            Combined Locator
        
        Examples:
            combine(parent_loc, child_loc) -> "parent child"
            combine(loc1, ">", loc2) -> "parent > child"
        """
        css_parts = []
        
        for loc in locators:
            if isinstance(loc, Locator):
                if loc.how != "css":
                    raise ValueError(f"Can only combine CSS locators, got {loc.how}")
                css_parts.append(loc.what)
            elif isinstance(loc, str):
                css_parts.append(loc)
            else:
                raise TypeError(f"Invalid locator type: {type(loc)}")
        
        combined_css = separator.join(css_parts)
        return Locator("css", combined_css)
    
    @staticmethod
    def descendant(parent: Locator, child: Locator) -> Locator:
        """Create descendant selector (parent child)."""
        return LocatorCombiner.combine(parent, child, separator=" ")

    @staticmethod
    def nested(*locators: Union[Locator, str]) -> Locator:
        """Create nested selector (parent child grandchild...).
        
        Args:
            *locators: Multiple locators or strings to combine as nested elements
            
        Returns:
            Combined Locator with nested relationship
            
        Examples:
            nested(parent, child) -> "parent child"  
            nested(grandparent, parent, child) -> "grandparent parent child"
            nested("div", ".class", "#id") -> "div .class #id"
            nested(CSS("div"), ".class", CSS("#id")) -> "div .class #id"
        """
        return LocatorCombiner.combine(*locators, separator=" ")
    
    @staticmethod
    def child(parent: Locator, child: Locator) -> Locator:
        """Create direct child selector (parent > child)."""
        return LocatorCombiner.combine(parent, child, separator=" > ")
    
    @staticmethod
    def sibling(first: Locator, second: Locator) -> Locator:
        """Create adjacent sibling selector (first + second)."""
        return LocatorCombiner.combine(first, second, separator=" + ")
    
    @staticmethod
    def or_selector(*locators: Locator) -> Locator:
        """Create OR selector (loc1, loc2, loc3)."""
        return LocatorCombiner.combine(*locators, separator=", ")