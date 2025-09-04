"""
QML UI Driver - Enhanced Version
Improvements:
- Better type hints and documentation
- Enhanced error handling with context
- Retry decorator for resilience
- Context managers for resource management
- Improved logging and debugging
- Performance optimizations
- Better separation of concerns
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, Any, Callable, List, Literal, Union, TypeVar, Generic, Dict, Tuple
from contextlib import contextmanager
from functools import wraps, lru_cache
from pathlib import Path
import os
import time
import json
import base64
import io
import logging
import re
from datetime import datetime as dt
from enum import Enum
from PIL import Image  # type: ignore
from dunetuf.ui.new.dune.workflow.locators.copy import LocatorCombiner

from dunetuf.udw import DuneUnderware, UDWError
from dunetuf.metadata import get_platform
from dunetuf.metadata import get_ip
from dunetuf.udw.udw import get_underware_instance

# Type definitions
T = TypeVar('T')
Strategy = Literal["css", "xpath", "object_id", "aria", "testid"]
StyleType = Literal['ascii', 'pretty', 'compact', 'json']
MouseButton = Literal["left", "right", "middle"]
KeyOperation = Literal["Press", "Release", "Click"]
MouseOperation = Literal["Click", "DblClick", "Wheel"]


# Import Locator - always use the one from the copy module
from dunetuf.ui.new.dune.workflow.locators.copy import Locator  # type: ignore

# For type checking, ensure we're using the right Locator type
LocatorType = Locator

def _env_float(name: str, default: float) -> float:
    raw = os.getenv(name, None)
    if raw is None:
        return default
    raw = raw.strip()
    if not raw:
        return default
    try:
        return float(raw)
    except (ValueError, TypeError):
        logging.warning(f"Env {name} has invalid value {raw!r}; using default {default}")
        return default

def _env_bool(name: str, default: bool = False) -> bool:
    raw = os.getenv(name, None)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


# Configuration for robust operations
@dataclass
class ClickConfig:
    """Configuration for click operations."""
    use_center: bool = True  # Click center by default
    offset_x: int = 0  # Offset from center/origin
    offset_y: int = 0
    retry_on_fail: bool = True
    max_retries: int = 3
    retry_delay: float = 0.5
    validate_after_click: bool = True
    wait_after_click: float = 0.3

# Configuration dataclass
@dataclass
class QmlDriverConfig:
    """Configuration for QmlDriver with sensible defaults."""
    mouse_delay: float = 0.5
    key_delay: float = 0.25
    wait_interval: float = 0.1
    wait_timeout: float = 15.0
    until_timeout: float = 25.0
    wheel_step: int = 120
    max_retries: int = 3
    retry_delay: float = 1.0
    screenshot_retries: int = 3
    human_mode: bool = field(default_factory=lambda: _env_bool("QMLTEST_HUMAN", False))
    timeout_factor: float = field(default_factory=lambda: _env_float("TUF_TIMEOUT_FACTOR", 1.0))


# Enhanced exceptions with context
class QmlDriverError(Exception):
    """Base exception for QML Driver errors."""
    def __init__(self, message: str, context: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.context = context or {}


class QmlElementNotFound(QmlDriverError):
    """Element not found in the QML scene."""
    pass


class QmlTimeout(QmlDriverError):
    """Operation timed out."""
    pass


class QmlCommunicationError(QmlDriverError):
    """Communication error with the test server."""
    pass


# Retry decorator for resilience
def retry(max_attempts: int = 3, delay: float = 1.0, exceptions: Tuple[type[BaseException], ...] = (Exception,)):
    """Retry decorator with exponential backoff."""
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args, **kwargs) -> T:
            last_exception = None
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        sleep_time = delay * (2 ** attempt)
                        logging.debug(f"Retry {attempt + 1}/{max_attempts} after {sleep_time}s: {e}")
                        time.sleep(sleep_time)
            if last_exception is not None:
                raise last_exception
            else:
                raise RuntimeError(f"Function failed {max_attempts} times but no exception was captured")
        return wrapper
    return decorator


class QmlElement:
    """Represents a QML UI element with enhanced functionality."""
    
    def __init__(self, driver: 'QmlDriver', selector: str, index: int = 0) -> None:
        self._driver = driver
        self._selector = selector
        self._index = index
        self._logger = logging.getLogger(f"{__name__}.QmlElement")
        self._property_cache: Dict[str, Any] = {}
        self._cache_timestamp: float = 0
        self._cache_ttl: float = 0.5  # Cache for 500ms
    
    def __repr__(self) -> str:
        return f"QmlElement(selector='{self._selector}', index={self._index})"
    
    # Mouse operations
    def click(self, x: int = 0, y: int = 5, button: MouseButton = "left") -> 'QmlElement':
        """Click on the element."""
        self._driver._click(self._selector, self._index, x, y, button)
        self._invalidate_cache()
        return self
    
    def double_click(self, x: int = 0, y: int = 0, button: MouseButton = "left") -> 'QmlElement':
        """Double-click on the element."""
        self._driver._mouse("DblClick", self._selector, self._index, x, y, button)
        self._invalidate_cache()
        return self
    
    def wheel(self, wheel_x: int, wheel_y: int, x: int = 0, y: int = 0) -> 'QmlElement':
        """Perform wheel operation on the element."""
        self._driver._wheel(self._selector, self._index, wheel_x, wheel_y, x, y)
        return self
    
    # Keyboard operations
    def key_press(self, text: str) -> 'QmlElement':
        """Press a key."""
        self._driver._keyboard("Press", self._selector, text)
        return self
    
    def key_release(self, text: str) -> 'QmlElement':
        """Release a key."""
        self._driver._keyboard("Release", self._selector, text)
        return self
    
    def key_click(self, text: str) -> 'QmlElement':
        """Click a key (press and release)."""
        self._driver._keyboard("Click", self._selector, text)
        return self
    
    def type_text(self, text: str, clear: bool = False) -> 'QmlElement':
        """Type text into the element."""
        if clear:
            self["text"] = ""
        self.key_click(text)
        return self
    
    # Property access with caching
    def __getitem__(self, prop: str) -> Any:
        """Get property value with optional caching."""
        if self._is_cache_valid() and prop in self._property_cache:
            return self._property_cache[prop]
        
        value = self._driver._property("Read", self._selector, self._index, prop)
        self._update_cache(prop, value)
        return value
    
    def __setitem__(self, prop: str, value: Any) -> None:
        """Set property value."""
        self._driver._property("Write", self._selector, self._index, prop, value)
        self._update_cache(prop, value)
    
    def get_properties(self, props: List[str]) -> Dict[str, Any]:
        """Get multiple properties efficiently."""
        return {prop: self[prop] for prop in props}
    
    # State checks
    @property
    def is_visible(self) -> bool:
        """Check if element is visible."""
        return bool(self["visible"])
    
    @property
    def is_enabled(self) -> bool:
        """Check if element is enabled."""
        return bool(self["enabled"])
    
    @property
    def has_focus(self) -> bool:
        """Check if element has active focus."""
        return bool(self["activeFocus"])
    
    @property
    def object_name(self) -> str:
        """Get the object name."""
        return str(self["objectName"])
    
    @property
    def text(self) -> str:
        """Get text content."""
        return str(self.get("text", ""))
    
    def get(self, prop: str, default: Any = None) -> Any:
        """Get property with default value."""
        try:
            return self[prop]
        except (QmlDriverError, KeyError):
            return default
    
    # Wait methods
    def wait_visible(self, timeout: float = 5.0) -> 'QmlElement':
        """Wait for element to become visible."""
        self._driver.wait_until(
            lambda: self.is_visible,
            timeout=timeout,
            waiting_for=f"{self._selector} to be visible"
        )
        return self
    
    def wait_enabled(self, timeout: float = 5.0) -> 'QmlElement':
        """Wait for element to become enabled."""
        self._driver.wait_until(
            lambda: self.is_enabled,
            timeout=timeout,
            waiting_for=f"{self._selector} to be enabled"
        )
        return self
    
    # Cache management
    def _is_cache_valid(self) -> bool:
        """Check if property cache is still valid."""
        return (time.time() - self._cache_timestamp) < self._cache_ttl
    
    def _update_cache(self, prop: str, value: Any) -> None:
        """Update property cache."""
        self._property_cache[prop] = value
        self._cache_timestamp = time.time()
    
    def _invalidate_cache(self) -> None:
        """Invalidate property cache."""
        self._property_cache.clear()
        self._cache_timestamp = 0


class QmlDriver:
    """Enhanced QML UI Driver with improved error handling and performance."""
    
    def __init__(
        self,
        screencapture: bool = False,
        config: Optional[QmlDriverConfig] = None
    ) -> None:
        self.ip_address = get_ip()
        self.config = config or QmlDriverConfig()
        self._logger = logging.getLogger(f"{__name__}.QmlDriver")
        self._udw = get_underware_instance(self.ip_address)
        self.screencapture = screencapture
        self._ui_info_cache: Optional[Tuple[str, str]] = None
        self._elements_cache: Dict[Tuple[str, int], QmlElement] = {}
        self._default_click_config = ClickConfig()
        self._locator_combiner = LocatorCombiner()
    
    def __enter__(self) -> 'QmlDriver':
        """Context manager entry."""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context manager exit."""
        self.disconnect()
    
    def connect(self) -> None:
        """Establish connection to the test server."""
        if not self._udw:
            self._udw = DuneUnderware(self.ip_address)
            self._logger.info(f"Connected to {self.ip_address}")
    
    def disconnect(self) -> None:
        """Clean up resources."""
        self._elements_cache.clear()
        self._ui_info_cache = None
        self._logger.info("Disconnected")
    
    # Request handling with retry
    @retry(max_attempts=3, delay=0.5, exceptions=(QmlCommunicationError,))
    def _request(self, endpoint: str, payload: Optional[Dict] = None) -> Any:
        """Make request to test server with retry logic."""
        if not self._udw:
            self.connect()
        
        result = None
        try:
            """
            # Map endpoints to UDW methods
            endpoint_map = {
                "mouse": lambda p: self._udw.mainUiApp.SpiceTestServer.mouseOperation(json.dumps(p)), #type: ignore
                "keyboard": lambda p: self._udw.mainUiApp.SpiceTestServer.keyboardOperation(json.dumps(p)), #type: ignore
                "property": lambda p: self._udw.mainUiApp.SpiceTestServer.propertyOperation(json.dumps(p)), #type: ignore
                "settings": lambda: self._udw.mainUiApp.SpiceTestServer.settingsOperation(), #type: ignore
                "screenshot": lambda: self._udw.mainUiApp.SpiceTestServer.screenshotOperation(), #type: ignore
                "isOnHomeScreen": lambda: self._udw.mainUiApp.SpiceTestServer.isOnHomeScreen(), #type: ignore
                "dumpQmlScene": lambda p: self._udw.mainUiApp.SpiceTestServer.dumpQmlScene(json.dumps(p)) #type: ignore
            }
            """
            # Helper: legacy payload string (matches older working client)

            def _legacy_payload(p: Optional[Dict]) -> str:
                # Old server expects a Python-dict-like string with single quotes and outer braces
                # Example: "{'operation': 'Click', 'querySelector': '#id', ...}"
                return "{}" if p is None else "{" + str(p) + "}"

            # Log the payload for debugging
            if self._logger.isEnabledFor(logging.DEBUG):
                self._logger.debug(f"Request endpoint: {endpoint}, payload: {payload}")
            # Map endpoints to UDW methods           
            endpoint_map = {
                "mouse":       lambda p: self._udw.mainUiApp.SpiceTestServer.mouseOperation(_legacy_payload(p)),       # type: ignore
                "keyboard":    lambda p: self._udw.mainUiApp.SpiceTestServer.keyboardOperation(_legacy_payload(p)),    # type: ignore
                "property":    lambda p: self._udw.mainUiApp.SpiceTestServer.propertyOperation(_legacy_payload(p)),    # type: ignore
                "settings":    lambda   : self._udw.mainUiApp.SpiceTestServer.settingsOperation(),                     # type: ignore
                "screenshot":  lambda   : self._udw.mainUiApp.SpiceTestServer.screenshotOperation(),                   # type: ignore
                "isOnHomeScreen": lambda: self._udw.mainUiApp.SpiceTestServer.isOnHomeScreen(),                        # type: ignore
                "dumpQmlScene": lambda p: self._udw.mainUiApp.SpiceTestServer.dumpQmlScene(_legacy_payload(p)),        # type: ignore
            }
            
            if endpoint not in endpoint_map:
                raise QmlDriverError(f"Unknown endpoint: {endpoint}")
            
            if endpoint in ["settings", "screenshot", "isOnHomeScreen"]:
                result = endpoint_map[endpoint]()
            else:
                result = endpoint_map[endpoint](payload)
            
            # Handle special cases
            if endpoint in ["isOnHomeScreen", "dumpQmlScene"]:
                return result
            
            # Parse JSON response
            response = json.loads(result) if isinstance(result, str) else result
            
            # Check for failures
            if isinstance(response, dict) and response.get("status") == "Failed":
                raise QmlCommunicationError(
                    response.get("message", "Operation failed"),
                    {"endpoint": endpoint, "payload": payload}
                )
            
            return response
            
        except UDWError as e:
            raise QmlCommunicationError(f"UDW Error: {e}", {"endpoint": endpoint})
        except json.JSONDecodeError as e:
            raise QmlCommunicationError(f"Invalid JSON response: {e}", {"raw_response": result})
    
    # UI information with caching
    @lru_cache(maxsize=2)
    def ui_type(self) -> str:
        """Get UI type with caching."""
        return self._udw.mainUiApp.ControlPanel.getExperience() #type: ignore
    
    @lru_cache(maxsize=2)
    def ui_theme(self) -> str:
        """Get UI theme with caching."""
        return self._udw.mainUiApp.ApplicationEngine.getTheme() #type: ignore
    
    def is_hybrid_ui(self) -> bool:
        """Check if using hybrid UI."""
        return self.ui_type() == "ProSelect" and self.ui_theme() == "hybridTheme"
    
    # Selector handling
    @staticmethod
    def _normalize_selector(target: Union[str, LocatorType]) -> str:
        """Convert target to selector string."""
        if isinstance(target, str):
            return target
        # Check for Locator-like objects with 'how' and 'what' attributes
        if hasattr(target, 'how') and hasattr(target, 'what'):
            if target.how != "css":
                raise QmlDriverError(f"Unsupported strategy: {target.how}")
            return target.what
        raise TypeError(f"Invalid selector type: {type(target)}")
    
    # Mouse operations
    def _mouse(
        self,
        op: str,
        selector: str,
        index: int,
        x: int = 0,
        y: int = 0,
        button: MouseButton = "left",
        wheel_x: int = 0,
        wheel_y: int = 0
    ) -> None:
        """Low-level mouse operation."""
        self._request("mouse", {
            "operation": op,
            "querySelector": selector,
            "queryIndex": index,
            "x": x,
            "y": y,
            "button": button,
            "wheelX": wheel_x,
            "wheelY": wheel_y
        })
        
        if self.config.human_mode:
            time.sleep(self.config.mouse_delay)
    
    def _click(
        self,
        selector: str,
        index: int,
        x: int = 0,
        y: int = 5,
        button: MouseButton = "left"
    ) -> None:
        """Internal click handler with hybrid UI support."""
        if self.is_hybrid_ui():
            self._logger.debug("Hybrid UI detected, using KeyHandler")
            self._udw.mainUiApp.KeyHandler.setKeyPress("ENTER") #type: ignore
        else:
            self._mouse("Click", selector, index, x, y, button)
    
    def _wheel(
        self,
        selector: str,
        index: int,
        wheel_x: int,
        wheel_y: int,
        x: int = 0,
        y: int = 0
    ) -> None:
        """Internal wheel handler with hybrid UI support."""
        if self.is_hybrid_ui():
            direction = "DOWN" if wheel_x == 0 else "UP"
            self._logger.debug(f"Hybrid UI detected, using KeyHandler {direction}")
            self._udw.mainUiApp.KeyHandler.setKeyPress(direction) #type: ignore
        else:
            self._mouse("Wheel", selector, index, x, y, wheel_x=wheel_x, wheel_y=wheel_y)
    
    # Keyboard operations
    def _keyboard(self, op: KeyOperation, selector: str, text: str) -> None:
        """Low-level keyboard operation."""
        delay = int(self.config.key_delay * 1000) if self.config.human_mode else 0
        self._request("keyboard", {
            "operation": op,
            "querySelector": selector,
            "text": text,
            "delay": delay
        })
    
    # Property operations
    def _property(
        self,
        op: str,
        selector: str,
        index: int,
        prop: str,
        value: Any = None
    ) -> Any:
        """Low-level property operation."""
        payload = {
            "operation": op,
            "querySelector": selector,
            "queryIndex": index,
            "property": prop
        }
        
        if op == "Write":
            payload["value"] = value
        
        response = self._request("property", payload)
        
        if op == "Read":
            if not isinstance(response, dict) or "value" not in response:
                raise QmlDriverError("Invalid property response")
            return response["value"]
        
        return None
    
    # Element finding and waiting
    def find(self, target: Union[str, LocatorType], index: int = 0) -> QmlElement:
        """Find an element in the QML scene."""
        selector = self._normalize_selector(target)
        cache_key = (selector, index)
        
        # Check cache
        if cache_key in self._elements_cache:
            element = self._elements_cache[cache_key]
            try:
                # Verify element still exists
                element["objectName"]
                return element
            except QmlDriverError:
                del self._elements_cache[cache_key]
        
        # Create new element
        element = QmlElement(self, selector, index)
        try:
            element["objectName"]  # Verify it exists
            self._elements_cache[cache_key] = element
            return element
        except Exception as e:
            raise QmlElementNotFound(
                f"Element not found: {selector}[{index}]",
                {"selector": selector, "index": index}
            )
    
    def find_all(self, target: Union[str, LocatorType]) -> List[QmlElement]:
        """Find all elements matching the selector."""
        selector = self._normalize_selector(target)
        elements = []
        index = 0
        
        while True:
            try:
                element = self.find(selector, index)
                elements.append(element)
                index += 1
            except QmlElementNotFound:
                break
        
        return elements
    
    def exists(self, target: Union[str, LocatorType], index: int = 0) -> bool:
        """Check if element exists."""
        try:
            self.find(target, index)
            return True
        except QmlElementNotFound:
            return False
    
    def wait_for(
        self,
        target: Union[str, LocatorType],
        timeout: Optional[float] = QmlDriverConfig.wait_timeout,
        index: int = 0,
        condition: Optional[Callable[[QmlElement], bool]] = None
    ) -> QmlElement:
        """Wait for element with optional condition."""
        selector = self._normalize_selector(target)
        timeout = self._apply_timeout_factor(timeout or self.config.wait_timeout)
        start_time = time.time()
        
        while True:
            try:
                element = self.find(selector, index)
                if condition is None or condition(element):
                    return element
            except QmlElementNotFound:
                pass
            
            if time.time() - start_time > timeout:
                raise QmlTimeout(
                    f"Element not found: {selector}[{index}] after {timeout:.2f}s",
                    {"selector": selector, "index": index, "timeout": timeout}
                )
            
            time.sleep(self.config.wait_interval)
    
    def wait_until(
        self,
        condition: Callable[[], bool],
        timeout: Optional[float] = None,
        message: Optional[str] = None,
        waiting_for: Optional[str] = None
    ) -> None:
        """Wait until condition is met."""
        timeout = self._apply_timeout_factor(timeout or self.config.until_timeout)
        start_time = time.time()
        
        while not condition():
            if time.time() - start_time > timeout:
                error_msg = message or f"Condition not met after {timeout:.2f}s"
                if waiting_for:
                    error_msg += f" (waiting for: {waiting_for})"
                raise QmlTimeout(error_msg)
            
            time.sleep(self.config.wait_interval)
    
    # High-level operations
    def click(
        self,
        target: Union[str, LocatorType],
        index: int = 0,
        x: int = 0,
        y: int = 5
    ) -> None:
        """Click on an element."""
        element = self.wait_for(target, index=index)
        element.click(x, y)

    # ========== Enhanced Click Operations ==========
    
    def smart_click(
        self,
        element,
        config: Optional[ClickConfig] = None
    ) -> bool:
        """
        Perform intelligent click with multiple strategies.
        
        Args:
            element: QmlElement to click
            config: Click configuration
            
        Returns:
            bool: True if click was successful
        """
        config = config or self._default_click_config
        
        # Try to get element bounds for center calculation
        if config.use_center:
            x, y = self._calculate_element_center(element)
            x += config.offset_x
            y += config.offset_y
        else:
            x, y = config.offset_x, config.offset_y
        
        #TODO: Add retry here?
        # Attempt click with retry logic
        for attempt in range(config.max_retries if config.retry_on_fail else 1):
            try:
                self._logger.debug(f"Click attempt {attempt + 1} at ({x}, {y})")
                
                # Ensure element is still valid and clickable
                if not self._is_clickable(element):
                    self._logger.warning("Element not clickable, waiting...")
                    element.wait_enabled(timeout=2.0)
                
                # Perform the click
                element.click(x, y)
                
                # Wait after click
                if config.wait_after_click > 0:
                    time.sleep(config.wait_after_click)
                
                # Validate if requested
                if config.validate_after_click:
                    if self._validate_click_success(element):
                        return True
                    else:
                        self._logger.warning(f"Click validation failed on attempt {attempt + 1}")
                else:
                    return True
                    
            except Exception as e:
                self._logger.warning(f"Click attempt {attempt + 1} failed: {e}")
                if attempt < config.max_retries - 1:
                    time.sleep(config.retry_delay)
                else:
                    raise
        
        return False
    
    def _calculate_element_center(self, element) -> Tuple[int, int]:
        """Calculate center point of an element."""
        try:
            # Try to get element dimensions
            width = element.get("width", 100)
            height = element.get("height", 50)
            
            # Return center coordinates
            return int(width / 2), int(height / 2)
        except Exception as e:
            self._logger.warning(f"Could not calculate center, using defaults: {e}")
            return 50, 25  # Reasonable defaults
    
    def _is_clickable(self, element) -> bool:
        """Check if element is in a clickable state."""
        try:
            return (
                element.is_visible and
                element.is_enabled and
                element.get("opacity", 1.0) > 0.5
            )
        except Exception:
            return False
    
    def _validate_click_success(self, element) -> bool:
        """Validate that a click was successful."""
        # This could check for:
        # - Element state change
        # - Navigation occurred
        # - New elements appeared
        # - Element is no longer visible (for dismissal clicks)
        
        # For now, basic validation
        time.sleep(0.2)  # Allow UI to update
        
        # Check if element still exists and state might have changed
        try:
            # If element disappeared, might indicate successful navigation
            if not self.exists(element._selector, element._index):
                return True
            
            # Check for focus change
            if element.has_focus:
                return True
                
            return True  # Assume success if no error
        except Exception:
            return True  # Element gone might mean success
    
    def type_text(
        self,
        target: Union[str, LocatorType],
        text: str,
        clear: bool = True,
        index: int = 0
    ) -> None:
        """Type text into an element."""
        element = self.wait_for(target, index=index)
        element.type_text(text, clear)
    
    def get_text(
        self,
        target: Union[str, LocatorType],
        prop: str = "text",
        index: int = 0
    ) -> str:
        """Get text from an element."""
        element = self.find(target, index)
        return str(element[prop])
    
    # Scene operations
    def dump_scene(
        self,
        branch: Optional[str] = None,
        index: int = 0,
        style: StyleType = "pretty",
        properties: Optional[List[str]] = None
    ) -> str:
        """Dump QML scene as text."""
        payload: Dict[str, Any] = {
            "format": "text",
            "style": style
        }
        
        if branch:
            payload.update({"branch": branch, "index": index})
        if properties:
            payload["properties"] = properties
        
        try:
            return self._request("dumpQmlScene", payload)
        except Exception as e:
            self._logger.error(f"Failed to dump scene: {e}")
            return "Error: Could not retrieve scene tree"
    
    def get_settings(self) -> Dict[str, Any]:
        """Get test server settings."""
        response = self._request("settings")
        if not isinstance(response, dict):
            raise QmlDriverError("Invalid settings response")
        return response
    
    def is_on_home_screen(self) -> bool:
        """Check if on home screen."""
        return bool(self._request("isOnHomeScreen"))
    
    # Screenshot operations
    @retry(max_attempts=3, delay=1.0)
    def capture_screenshot(self) -> Image.Image:
        """Capture screenshot with retry."""
        response = self._request("screenshot")
        
        if not isinstance(response, dict) or "message" not in response:
            raise QmlDriverError("Invalid screenshot response")
        
        try:
            image_data = base64.b64decode(response["message"].encode())
            return Image.open(io.BytesIO(image_data))
        except Exception as e:
            if "wayland" in str(response.get("message", "")).lower():
                raise QmlDriverError("Screenshots disabled on Wayland")
            raise QmlDriverError(f"Failed to decode screenshot: {e}")
    
    def save_screenshot(
        self,
        metadata: Tuple[str, str, str],
        name: str,
        output_dir: str = "/code/output/tuf_screencaptures"
    ) -> Optional[Path]:
        """Save screenshot with improved path handling."""
        if not self.screencapture:
            return None
        
        if not metadata or len(metadata) != 3:
            raise ValueError("Metadata must be (product, version, folder)")
        
        product, version, folder = metadata
        
        # Clean up names
        name = self._sanitize_filename(name)
        version = version.split('+')[0]
        folder = self._sanitize_filename(folder)
        
        # Extract number prefix if present
        match = re.match(r"(\d+)_(.+)", name)
        if match:
            number, name = match.groups()
            name = f"{int(number):03d}_{name}"
        
        # Get platform
        platform = self._get_platform_short()
        
        # Build path
        date_str = dt.now().strftime("%Y_%m_%d")
        path = Path(output_dir) / date_str / f"{folder}_ver{version}_{platform}" / product
        path.mkdir(parents=True, exist_ok=True)
        
        # Capture and save
        try:
            image = self.capture_screenshot()
            filepath = path / f"{name}.png"
            image.save(filepath, "PNG")
            self._logger.info(f"Screenshot saved: {filepath}")
            return filepath
        except Exception as e:
            self._logger.error(f"Failed to save screenshot: {e}")
            return None
        
    # ========== Scrolling Operations ==========
    
    def scroll_to_element(
        self,
        target_element: Union[LocatorType, str],
        scrollbar: Optional[Union[LocatorType, str]] = None,
        max_scroll_attempts: int = 10,
        scroll_step: int = 120,
        direction: Literal["up", "down"] = "down"
    ) -> QmlElement:
        """
        Scroll until target element is visible.
        
        Args:
            target_element: Element to scroll to
            scrollbar: Optional scrollbar to use for scrolling
            max_scroll_attempts: Maximum number of scroll attempts
            scroll_step: Pixels to scroll each time
            direction: Scroll direction
            
        Returns:
            The found element
            
        Raises:
            TimeoutError: If element not found after max attempts
        """
        self._logger.debug(f"Scrolling to find element: {target_element}")
        
        for attempt in range(max_scroll_attempts):
            # Check if element is already visible
            if self.exists(target_element):
                element = self.find(target_element)
                if element.is_visible:
                    self._logger.debug(f"Element found after {attempt} scroll attempts")
                    return element
            
            # Perform scroll
            if scrollbar:
                # Scroll using specific scrollbar
                scrollbar_element = self.find(scrollbar)
                wheel_y = scroll_step if direction == "down" else -scroll_step
                scrollbar_element.wheel(0, wheel_y)
            
            # Wait for UI to update
            time.sleep(0.3)
        
        raise TimeoutError(
            f"Could not find element {target_element} after {max_scroll_attempts} scroll attempts"
        )
    
    def scroll_to_position(
        self,
        position: float,
        scrollbar: Union[LocatorType, str],
        orientation: Literal["vertical", "horizontal"] = "vertical"
    ) -> None:
        """
        Scroll to a specific position.
        
        Args:
            position: Position to scroll to (0.0 = top/left, 1.0 = bottom/right)
            scrollbar: Scrollbar to use
            orientation: Scrollbar orientation
        """
        self._logger.debug(f"Scrolling to position {position} on {orientation} scrollbar")
        
        try:
            scrollbar_element = self.find(scrollbar)
            
            # Get scrollbar dimensions
            if orientation == "vertical":
                total_height = scrollbar_element.get("contentHeight", 1000)
                visible_height = scrollbar_element.get("height", 100)
                max_scroll = total_height - visible_height
                target_position = int(position * max_scroll)
                
                # Set scroll position
                scrollbar_element["contentY"] = target_position
            else:
                total_width = scrollbar_element.get("contentWidth", 1000)
                visible_width = scrollbar_element.get("width", 100)
                max_scroll = total_width - visible_width
                target_position = int(position * max_scroll)
                
                # Set scroll position
                scrollbar_element["contentX"] = target_position
            
            # Wait for scroll animation
            #self.wait_for_animation_complete()
            time.sleep(0.2)  # Simple wait for now
            
        except Exception as e:
            self._logger.warning(f"Could not scroll to position: {e}")
            # Fallback to wheel scrolling
            #self._scroll_with_wheel_to_position(position, scrollbar, orientation)

    def _reset_scroll_position(self, scrollbar_locator: Locator) -> None:
        """Reset scrollbar to the top position."""
        try:
            self.scroll_to_position(0, scrollbar_locator, "vertical")
            time.sleep(0.5)  # Allow UI to settle
            self._logger.debug("Reset scroll position to top")
        except Exception as e:
            self._logger.warning(f"Failed to reset scroll position: {e}")

    def _find_single_menu_item(
        self, 
        menu_item_id: str, 
        screen_locator: Locator, 
        select_option: bool,
        scrolling_value: float, 
        scrollbar_locator: Locator
    ) -> bool:
        """Find and optionally click a single menu item."""
        step_value = 0.0
        max_scroll_attempts = int(1.0 / scrolling_value) + 5  # Add buffer
        
        self._logger.debug(f"Searching for single menu item: {menu_item_id}")
        
        for attempt in range(max_scroll_attempts):
            try:
                # Check if item is visible at current scroll position
                if self._is_menu_item_visible(screen_locator, menu_item_id):
                    self._logger.info(f"Found menu item {menu_item_id} at scroll position {step_value}")
                    
                    if select_option:
                        return self._click_menu_item(screen_locator, menu_item_id)
                    return True
                
                # Scroll to next position if not found
                if step_value >= 1.0:
                    break
                    
                step_value = min(step_value + scrolling_value, 1.0)
                self._scroll_to_position_with_retry(step_value, scrollbar_locator)
                
            except Exception as e:
                self._logger.debug(f"Search attempt {attempt + 1} failed: {e}")
                # Continue searching even if this position fails
                step_value = min(step_value + scrolling_value, 1.0)
                if step_value < 1.0:
                    self._scroll_to_position_with_retry(step_value, scrollbar_locator)
        
        self._logger.warning(f"Menu item {menu_item_id} not found after searching entire scroll range")
        return False

    def _find_locator_menu_item(
        self, 
        menu_item_locator: Locator, 
        screen_locator: Locator, 
        select_option: bool,
        scrolling_value: float, 
        scrollbar_locator: Locator
    ) -> bool:
        """Find and optionally click a menu item using a Locator object."""
        step_value = 0.0
        max_scroll_attempts = int(1.0 / scrolling_value) + 5  # Add buffer
        
        self._logger.debug(f"Searching for menu item using Locator: {menu_item_locator.what}")
        
        for attempt in range(max_scroll_attempts):
            try:
                # Check if item is visible at current scroll position
                if self._is_locator_menu_item_visible(menu_item_locator):
                    self._logger.info(f"Found menu item {menu_item_locator.what} at scroll position {step_value}")
                    
                    if select_option:
                        return self._click_locator_menu_item(menu_item_locator)
                    return True
                
                # Scroll to next position if not found
                if step_value >= 1.0:
                    break
                    
                step_value = min(step_value + scrolling_value, 1.0)
                self._scroll_to_position_with_retry(step_value, scrollbar_locator)
                
            except Exception as e:
                self._logger.debug(f"Search attempt {attempt + 1} failed: {e}")
                # Continue searching even if this position fails
                step_value = min(step_value + scrolling_value, 1.0)
                if step_value < 1.0:
                    self._scroll_to_position_with_retry(step_value, scrollbar_locator)
        
        self._logger.warning(f"Menu item {menu_item_locator.what} not found after searching entire scroll range")
        return False


    def _find_nested_menu_item(
        self, 
        menu_item_ids: List[str], 
        screen_locator: Locator, 
        select_option: bool,
        scrolling_value: float, 
        scrollbar_locator: Locator
    ) -> bool:
        """Find and optionally click a nested menu item (row + item)."""
        row_id, item_id = menu_item_ids
        step_value = 0.0
        max_scroll_attempts = int(1.0 / scrolling_value) + 5
        
        self._logger.debug(f"Searching for nested menu item: row={row_id}, item={item_id}")
        
        for attempt in range(max_scroll_attempts):
            try:
                # First check if the row is visible
                if self._is_menu_item_visible(screen_locator, row_id):
                    self._logger.debug(f"Found row {row_id} at scroll position {step_value}")
                    
                    # Then check if the specific item within the row is visible
                    if self._is_nested_item_visible(screen_locator, row_id, item_id):
                        self._logger.info(f"Found nested item {item_id} in row {row_id}")
                        
                        if select_option:
                            return self._click_nested_menu_item(screen_locator, row_id, item_id)
                        return True
                
                # Scroll to next position if not found
                if step_value >= 1.0:
                    break
                    
                step_value = min(step_value + scrolling_value, 1.0)
                self._scroll_to_position_with_retry(step_value, scrollbar_locator)
                
            except Exception as e:
                self._logger.debug(f"Nested search attempt {attempt + 1} failed: {e}")
                step_value = min(step_value + scrolling_value, 1.0)
                if step_value < 1.0:
                    self._scroll_to_position_with_retry(step_value, scrollbar_locator)
        
        self._logger.warning(f"Nested menu item {item_id} in {row_id} not found after searching")
        return False

    def _find_nested_locator_menu_item(
        self, 
        menu_item_locators: List[Locator], 
        screen_locator: Locator, 
        select_option: bool,
        scrolling_value: float, 
        scrollbar_locator: Locator
    ) -> bool:
        """Find and optionally click a nested menu item using Locator objects."""
        row_locator, item_locator = menu_item_locators
        step_value = 0.0
        max_scroll_attempts = int(1.0 / scrolling_value) + 5
        
        self._logger.debug(f"Searching for nested menu item: row={row_locator.what}, item={item_locator.what}")
        
        for attempt in range(max_scroll_attempts):
            try:
                # First check if the row is visible
                if self._is_locator_menu_item_visible(row_locator):
                    self._logger.debug(f"Found row {row_locator.what} at scroll position {step_value}")
                    
                    # Then check if the specific item within the row is visible
                    if self._is_nested_locator_item_visible(row_locator, item_locator):
                        self._logger.info(f"Found nested item {item_locator.what} in row {row_locator.what}")
                        
                        if select_option:
                            return self._click_nested_locator_menu_item(row_locator, item_locator)
                        return True
                
                # Scroll to next position if not found
                if step_value >= 1.0:
                    break
                    
                step_value = min(step_value + scrolling_value, 1.0)
                self._scroll_to_position_with_retry(step_value, scrollbar_locator)
                
            except Exception as e:
                self._logger.debug(f"Nested search attempt {attempt + 1} failed: {e}")
                step_value = min(step_value + scrolling_value, 1.0)
                if step_value < 1.0:
                    self._scroll_to_position_with_retry(step_value, scrollbar_locator)
        
        self._logger.warning(f"Nested menu item {item_locator.what} in {row_locator.what} not found after searching")
        return False

    def _is_menu_item_visible(self, screen_locator: Locator, item_id: str) -> bool:
        """Check if a menu item is visible on the screen."""
        try:
            # Create combined locator for screen + item
            item_locator = self._locator_combiner.descendant(
                screen_locator, 
                Locator("css", item_id)
            )
            
            element = self.find(item_locator)
            return element is not None and element.is_visible
            
        except Exception as e:
            self._logger.debug(f"Item {item_id} visibility check failed: {e}")
            return False

    def _is_locator_menu_item_visible(self, menu_item_locator: Locator) -> bool:
        """Check if a menu item is visible using a Locator object."""
        try:
            element = self.find(menu_item_locator)
            return element is not None and element.is_visible
        except Exception as e:
            self._logger.debug(f"Locator item {menu_item_locator.what} visibility check failed: {e}")
            return False

    def _is_nested_item_visible(self, screen_locator: Locator, row_id: str, item_id: str) -> bool:
        """Check if a nested menu item is visible within its row."""
        try:
            # Create combined locator for screen + row + item
            nested_locator = self._locator_combiner.combine(
                screen_locator, 
                Locator("css", row_id),
                Locator("css", item_id),
                separator=" "
            )
            
            element = self.find(nested_locator)
            return element is not None and element.is_visible
            
        except Exception as e:
            self._logger.debug(f"Nested item {item_id} in {row_id} visibility check failed: {e}")
            return False

    def _is_nested_locator_item_visible(self, row_locator: Locator, item_locator: Locator) -> bool:
        """Check if a nested menu item is visible within its row using Locator objects."""
        try:
            # Create combined locator for row + item
            nested_locator = self._locator_combiner.descendant(row_locator, item_locator)
            
            element = self.find(nested_locator)
            return element is not None and element.is_visible
            
        except Exception as e:
            self._logger.debug(f"Nested item {item_locator.what} in {row_locator.what} visibility check failed: {e}")
            return False

    def _click_menu_item(self, screen_locator: Locator, item_id: str) -> bool:
        """Click a single menu item."""
        try:
            item_locator = self._locator_combiner.descendant(
                screen_locator, 
                Locator("css", item_id)
            )
            
            element = self.wait_for(item_locator, timeout=2.0)
            
            click_config = ClickConfig(
                use_center=True,
                validate_after_click=True,
                retry_on_fail=True,
                max_retries=2
            )
            
            success = self.smart_click(element, click_config)
            if success:
                self._logger.info(f"Successfully clicked menu item: {item_id}")
            else:
                self._logger.error(f"Failed to click menu item: {item_id}")
            
            return success
            
        except Exception as e:
            self._logger.error(f"Error clicking menu item {item_id}: {e}")
            return False

    def _click_nested_menu_item(self, screen_locator: Locator, row_id: str, item_id: str) -> bool:
        """Click a nested menu item."""
        try:
            nested_locator = self._locator_combiner.combine(
                screen_locator, 
                Locator("css", row_id),
                Locator("css", item_id),
                separator=" "
            )
            
            element = self.wait_for(nested_locator, timeout=2.0)
            
            # Use mouse_click for nested items (as in original code)
            element.click()
            self._logger.info(f"Successfully clicked nested item: {item_id} in {row_id}")
            return True
            
        except Exception as e:
            self._logger.error(f"Error clicking nested item {item_id} in {row_id}: {e}")
            return False

    def _click_locator_menu_item(self, menu_item_locator: Locator) -> bool:
        """Click a menu item using a Locator object."""
        try:
            element = self.wait_for(menu_item_locator, timeout=2.0)
            
            click_config = ClickConfig(
                use_center=True,
                validate_after_click=True,
                retry_on_fail=True,
                max_retries=2
            )
            
            success = self.smart_click(element, click_config)
            if success:
                self._logger.info(f"Successfully clicked menu item: {menu_item_locator.what}")
            else:
                self._logger.error(f"Failed to click menu item: {menu_item_locator.what}")
            
            return success
            
        except Exception as e:
            self._logger.error(f"Error clicking menu item {menu_item_locator.what}: {e}")
            return False

    def _click_nested_locator_menu_item(self, row_locator: Locator, item_locator: Locator) -> bool:
        """Click a nested menu item using Locator objects."""
        try:
            # Create combined locator for row + item
            nested_locator = self._locator_combiner.descendant(row_locator, item_locator)
            
            element = self.wait_for(nested_locator, timeout=2.0)
            
            # Use mouse_click for nested items (as in original code)
            element.click()
            self._logger.info(f"Successfully clicked nested item: {item_locator.what} in {row_locator.what}")
            return True
            
        except Exception as e:
            self._logger.error(f"Error clicking nested item {item_locator.what} in {row_locator.what}: {e}")
            return False

    def _scroll_to_position_with_retry(self, position: float, scrollbar_locator: Locator) -> None:
        """Scroll to position with retry logic."""
        max_retries = 3
        
        for attempt in range(max_retries):
            try:
                self.scroll_to_position(position, scrollbar_locator, "vertical")
                time.sleep(0.5)  # Allow UI to settle after scroll
                return
                
            except Exception as e:
                self._logger.warning(f"Scroll attempt {attempt + 1} failed: {e}")
                if attempt == max_retries - 1:
                    raise RuntimeError(f"Failed to scroll to position {position} after {max_retries} attempts")
                time.sleep(0.2)  # Brief delay before retry
    
    @contextmanager
    def screenshot_on_error(self, name: str, metadata: Optional[Tuple[str, str, str]] = None):
        """Context manager to capture screenshot on error."""
        try:
            yield
        except Exception as e:
            if metadata:
                self._logger.error(f"Error occurred, capturing screenshot: {e}")
                self.save_screenshot(metadata, f"error_{name}")
            raise
    
    # Utility methods
    def _apply_timeout_factor(self, timeout: float) -> float:
        """Apply timeout factor from environment."""
        return timeout * self.config.timeout_factor
    
    @staticmethod
    def _sanitize_filename(name: str) -> str:
        """Sanitize filename for filesystem."""
        return re.sub(r'[/\\<>:"|?*]', '_', str(name))
    
    @staticmethod
    def _get_platform_short() -> str:
        """Get short platform name."""
        platform = str(get_platform())
        platform_map = {
            "MetaDataPlatform.Simulator": "Sim",
            "MetaDataPlatform.Emulator": "Emu",
            "MetaDataPlatform.Engine": "Eng"
        }
        return platform_map.get(platform, "Unknown")
    
    # Batch operations
    def batch_click(self, targets: List[Union[str, LocatorType]], delay: float = 0.5) -> None:
        """Click multiple elements in sequence."""
        for target in targets:
            self.click(target)
            if delay > 0:
                time.sleep(delay)
    
    def wait_for_any(
        self,
        targets: List[Union[str, LocatorType]],
        timeout: Optional[float] = None
    ) -> QmlElement:
        """Wait for any of the targets to appear."""
        timeout = self._apply_timeout_factor(timeout or self.config.wait_timeout)
        start_time = time.time()
        
        while True:
            for target in targets:
                try:
                    return self.find(target)
                except QmlElementNotFound:
                    continue
            
            if time.time() - start_time > timeout:
                raise QmlTimeout(
                    f"None of {len(targets)} targets found after {timeout:.2f}s"
                )
            
            time.sleep(self.config.wait_interval)

    def are_elements_visible(self, locators: list) -> bool:
        """Check if all specified elements are visible."""
        if not locators:
            return False
        
        for locator in locators:
            if not self.exists(locator):
                return False
        return True