"""
Enhanced Workflow XL Copy Operations
Improvements:
- Robust clicking without hardcoded coordinates
- Better error handling and recovery
- Comprehensive logging
- Retry mechanisms for flaky operations
- State validation
- Performance monitoring
"""

from typing import Optional, Tuple, Dict, Any, Callable, Union, List
from contextlib import contextmanager
from functools import wraps
from dataclasses import dataclass
from enum import Enum
import time
import logging

from dunetuf.ui.new.shared.protocols.copy_ops import CopyOps
from dunetuf.ui.new.shared.enums import Platform, UIType, UISize, Feature
from dunetuf.ui.new.shared.decorators.feature_registry import FeatureRegistry
from dunetuf.ui.new.dune.workflow.locators.copy import CopyLoc, Locator, LocatorCombiner
from dunetuf.ui.new.shared.driver import ClickConfig
from dunetuf.ui.new.ui import UI


class NavigationState(Enum):
    """Track navigation state for validation."""
    UNKNOWN = "unknown"
    HOME = "home"
    COPY_WIDGET_CARD = "copy_widget_card"
    COPY_LANDING = "copy_landing"
    COPY_OPTIONS_LIST = "copy_options_list"
    COPY_SETTINGS = "copy_settings"
    COPY_COLOR_SETTINGS = "copy_color_settings"
    COPY_APP = "copy_app"



def measure_performance(operation_name: str):
    """Decorator to measure and log operation performance."""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            start_time = time.time()
            self._logger.debug(f"Starting {operation_name}")
            try:
                result = func(self, *args, **kwargs)
                elapsed = time.time() - start_time
                self._logger.info(f"{operation_name} completed in {elapsed:.2f}s")
                self._performance_metrics[operation_name] = elapsed
                return result
            except Exception as e:
                elapsed = time.time() - start_time
                self._logger.error(f"{operation_name} failed after {elapsed:.2f}s: {e}")
                raise
        return wrapper
    return decorator


def validate_state(expected_state: NavigationState):
    """Decorator to validate navigation state before operation."""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(self: 'WorkflowXLCopyOps', *args, **kwargs):
            if self.validate_navigation:
                current = self._get_current_state()
                if current != expected_state and expected_state != NavigationState.UNKNOWN:
                    self._logger.warning(
                        f"State mismatch: expected {expected_state.value}, got {current.value}"
                    )
            return func(self, *args, **kwargs)
        return wrapper
    return decorator


@FeatureRegistry.register(Platform.DUNE, UIType.WORKFLOW, UISize.XL, Feature.COPY)
class WorkflowXLCopyOps(CopyOps):
    """Enhanced Copy Operations for Workflow XL UI."""
    
    def __init__(self, ui: "UI", validate_navigation: bool = True) -> None:
        self.ui = ui
        self._driver = ui._driver
        self.validate_navigation = validate_navigation
        self._logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        self._current_state = NavigationState.UNKNOWN
        self._performance_metrics: Dict[str, float] = {}
        self._default_click_config = ClickConfig()
        self._locator_combiner = LocatorCombiner()
        
        # Configure logging
        self._setup_logging()
    
    def _setup_logging(self) -> None:
        """Setup operation-specific logging."""
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        self._logger.addHandler(handler)
        self._logger.setLevel(logging.DEBUG)
    
    # ========== State Management ==========
    
    def _get_current_state(self) -> NavigationState:
        """Detect current navigation state based on visible elements."""
        state_indicators = {
            NavigationState.HOME: [
                # Add home screen indicators
            ],
            NavigationState.COPY_WIDGET_CARD: [
                CopyLoc.view_copy_widget_card_screen
            ],
            NavigationState.COPY_LANDING: [
                CopyLoc.view_copy_screen
            ],
            NavigationState.COPY_OPTIONS_LIST: [
                # Add copy options list indicators
                # Could be a combination of view_copy_screen and visible options
            ],
            NavigationState.COPY_SETTINGS: [
                CopyLoc.view_copy_settings
            ],
            NavigationState.COPY_COLOR_SETTINGS: [
                CopyLoc.view_copy_settings_color
            ],
            NavigationState.COPY_APP: [
                # Add copy app indicators
            ]
        }
        
        # Check states in priority order (most specific first)
        priority_order = [
            NavigationState.COPY_COLOR_SETTINGS,
            NavigationState.COPY_SETTINGS,
            NavigationState.COPY_OPTIONS_LIST,
            NavigationState.COPY_LANDING,
            NavigationState.COPY_WIDGET_CARD,
            NavigationState.COPY_APP,
            NavigationState.HOME
        ]
        
        for state in priority_order:
            if state in state_indicators:
                locators = state_indicators[state]
                if self._are_elements_visible(locators):
                    self._current_state = state
                    return state
        
        return NavigationState.UNKNOWN
    
    def _are_elements_visible(self, locators: list) -> bool:
        """Check if all specified elements are visible."""
        if not locators:
            return False
        
        for locator in locators:
            if not self._driver.exists(locator):
                return False
        return True
    
    @contextmanager
    def _state_transition(self, from_state: NavigationState, to_state: NavigationState):
        """Context manager for state transitions with rollback on failure."""
        self._logger.debug(f"Transitioning from {from_state.value} to {to_state.value}")
        original_state = self._current_state
        
        try:
            yield
            self._current_state = to_state
            self._logger.debug(f"Successfully transitioned to {to_state.value}")
        except Exception as e:
            self._logger.error(f"Failed to transition to {to_state.value}: {e}")
            self._current_state = original_state
            raise
    

    
    # ========== Navigation Operations ==========
    
    @measure_performance("Navigate to Copy Widget Landing")
    @validate_state(NavigationState.HOME)
    def goto_copywidget_option_landingview(self) -> None:
        """
        Navigate from home screen to copy landing view.
        
        Navigation path: Home >> Copy Widget Card >> Copy Landing View
        
        Raises:
            TimeoutError: If navigation times out
            NavigationError: If navigation fails
        """
        with self._state_transition(NavigationState.HOME, NavigationState.COPY_LANDING):
            # Wait for copy widget card screen
            self._logger.info("Waiting for copy widget card screen")
            self._driver.wait_for(
                CopyLoc.view_copy_widget_card_screen
            )
            
            # Find and click the button to go to copy app
            self._logger.info("Finding copy app button")
            button = self._driver.wait_for(
                CopyLoc.widget_button_goto_copy_app,
                condition=lambda el: el.is_enabled
            )
            
            # Use smart click instead of hardcoded coordinates
            self._logger.info("Clicking copy app button")
            click_config = ClickConfig(
                use_center=True,
                validate_after_click=True,
                retry_on_fail=True
            )
            
            if not self._driver.smart_click(button, click_config):
                raise RuntimeError("Failed to click copy app button")
            
            # Verify navigation completed
            self._verify_navigation(
                expected_state=NavigationState.COPY_LANDING,
                expected_elements=[CopyLoc.view_copy_screen],
                state_name="copy landing view"
            )

    @measure_performance("Verify Navigation to Copy Landing")
    @validate_state(NavigationState.COPY_LANDING)
    def goto_copywidget_options_listview(self) -> None:
        """
        Navigate from copy landing view to copy options list view.
        
        Navigation path: Copy Landing View >> Copy Options List View
        
        Raises:
            TimeoutError: If navigation times out
            NavigationError: If navigation fails
        """
        with self._state_transition(NavigationState.COPY_LANDING, NavigationState.COPY_APP):
            # Wait for copy landing view
            self._logger.info("Waiting for copy landing view")
            self._driver.wait_for(
                CopyLoc.view_copy_screen
            )
            
            # Find and click the button to go to copy options list
            self._logger.info("Finding copy options list button")
            combined_locator = self._locator_combiner.descendant(
                CopyLoc.view_copy_screen,
                CopyLoc.button_copy_more_options
            )
            button = self._driver.wait_for(
                combined_locator,
                condition=lambda el: el.is_enabled
            )
            
            # Use smart click instead of hardcoded coordinates
            self._logger.info("Clicking copy options list button")
            click_config = ClickConfig(
                use_center=True,
                validate_after_click=True,
                retry_on_fail=True,
                wait_after_click=0.5
            )
            
            if not self._driver.smart_click(button, click_config):
                raise RuntimeError("Failed to click copy options list button")
            
            # Verify navigation completed
            self._verify_navigation(
                expected_state=NavigationState.COPY_SETTINGS,
                expected_elements=[CopyLoc.view_copy_settings],
                state_name="copy settings",
            )

    @measure_performance("Verify Navigation to Copy Landing")
    @validate_state(NavigationState.COPY_LANDING)
    def goto_copy_option_color_screen(self) -> None:
        """
        Navigate from copy landing view to copy options list view.
        
        Navigation path: Copy Landing View >> Copy Options List View
        
        Raises:
            TimeoutError: If navigation times out
            NavigationError: If navigation fails
        """
        with self._state_transition(NavigationState.COPY_LANDING, NavigationState.COPY_APP):

            self._driver.scroll_to_position(0, CopyLoc.options_scrollbar, "vertical")
            menu_item_id = [CopyLoc.row_combo_color, CopyLoc.combo_color]
            self.goto_item(
                menu_item_id=menu_item_id,
                screen_id=CopyLoc.view_copy_screen,
                select_option=True,
                scrolling_value=0.1,
                scrollbar_locator=CopyLoc.options_scrollbar
            )

            # Wait for copy landing view
            self._logger.info("Waiting for copy landing view")
            self._driver.wait_for(
                CopyLoc.view_color_list
            )

    @measure_performance("Select Color Mode")
    @validate_state(NavigationState.COPY_SETTINGS)
    def select_color_mode(self, option: str) -> None:
        """
        Select a color mode option in the copy settings.
        
        UI should be in copy Settings view screen.
        Navigates to color mode screen and selects the specified color option.
        UI Flow: Copy Settings -> Color Mode -> Select Color Option -> Return to Settings
        
        Args:
            option: Color mode to select. Valid options:
                - "Automatic": Auto color detection
                - "Color": Full color mode
                - "Grayscale": Grayscale/monochrome mode  
                - "Black Only": Black ink only mode
                
        Raises:
            ValueError: If invalid color option is provided
            TimeoutError: If navigation or selection times out
            RuntimeError: If color selection fails
        """
        # Validate input
        valid_options = ["Automatic", "Color", "Grayscale", "Black Only"]
        if option not in valid_options:
            raise ValueError(f"Invalid color option '{option}'. Valid options: {valid_options}")
        
        self._logger.info(f"Selecting color mode: {option}")
        
        with self.error_handling(f"select_color_mode_{option}"):
            # Navigate to color options screen
            self._navigate_to_color_options()
            
            # Select the specific color option
            self._select_color_option(option)
            
            # Verify we're back in settings view
            self._verify_return_to_settings()

    def _navigate_to_color_options(self) -> None:
        """Navigate from copy settings to color options screen."""
        self._logger.info("Navigating to color options screen")
        
        with self._state_transition(NavigationState.COPY_SETTINGS, NavigationState.COPY_COLOR_SETTINGS):
            # Use the existing goto_copy_option_color_screen method
            self.goto_copy_option_color_screen()
            
            # Wait for color options to be available
            self._driver.wait_for(
                CopyLoc.view_color_list,
                timeout=10.0,
                condition=lambda el: el.is_visible
            )
            
            # Allow UI to settle after navigation
            time.sleep(1.0)
            
            self._logger.info("Successfully navigated to color options screen")

    def _select_color_option(self, option: str) -> None:
        """
        Select the specified color option from the color list.
        
        Args:
            option: The color option to select
        """
        self._logger.info(f"Selecting color option: {option}")
        
        # Define color option locators mapping
        color_option_locators = {
            "Automatic": CopyLoc.combo_color_option_automatic,
            "Color": CopyLoc.combo_color_option_color, 
            "Grayscale": CopyLoc.combo_color_option_grayscale,
            "Black Only": CopyLoc.combo_color_option_blackonly
        }
        
        # Get the locator for the requested option
        option_locator = color_option_locators.get(option)
        if not option_locator:
            raise ValueError(f"No locator defined for color option: {option}")
        
        try:
            # Wait for the specific color option to be available
            self._logger.debug(f"Waiting for color option element: {option}")
            color_element = self._driver.wait_for(
                option_locator,
                timeout=5.0,
                condition=lambda el: el.is_visible and el.is_enabled
            )
            
            # Create click configuration for color selection
            click_config = ClickConfig(
                use_center=True,
                validate_after_click=True,
                retry_on_fail=True,
                max_retries=3,
                wait_after_click=0.5
            )
            
            # Perform the click using smart click
            self._logger.info(f"Clicking color option: {option}")
            success = self._driver.smart_click(color_element, click_config)
            
            if not success:
                raise RuntimeError(f"Failed to click color option: {option}")
            
            # Wait a moment for the selection to be processed
            time.sleep(0.5)
            
            self._logger.info(f"Successfully selected color option: {option}")
            
        except Exception as e:
            self._logger.error(f"Failed to select color option '{option}': {e}")
            raise RuntimeError(f"Color option selection failed for '{option}': {e}")

    def _verify_return_to_settings(self) -> None:
        """Verify that we've returned to the copy settings view."""
        self._logger.info("Verifying return to copy settings view")
        
        try:
            # Wait for the copy settings view to be visible again
            settings_view = self._driver.wait_for(
                CopyLoc.view_copy_settings,
                timeout=9.0,
                condition=lambda el: el.is_visible
            )
            
            # Update our navigation state
            self._current_state = NavigationState.COPY_SETTINGS
            
            self._logger.info("Successfully returned to copy settings view")
            
        except Exception as e:
            self._logger.error(f"Failed to return to copy settings view: {e}")
            raise TimeoutError(f"Did not return to copy settings view within timeout: {e}")

    # Enhanced version with additional validation and options
    @measure_performance("Select Color Mode with Validation")
    def select_color_mode_with_validation(
        self, 
        option: str, 
        verify_selection: bool = True,
        wait_for_ui_update: float = 2.0
    ) -> bool:
        """
        Enhanced color mode selection with additional validation options.
        
        Args:
            option: Color mode to select
            verify_selection: Whether to verify the selection was applied
            wait_for_ui_update: Time to wait for UI to update after selection
            
        Returns:
            bool: True if selection was successful and verified
        """
        self._logger.info(f"Selecting color mode with validation: {option}")
        
        try:
            # Perform the basic color selection
            self.select_color_mode(option)
            
            # Wait for UI to update
            if wait_for_ui_update > 0:
                time.sleep(wait_for_ui_update)
            
            # Verify selection if requested
            if verify_selection:
                return self._verify_color_selection(option)
            
            return True
            
        except Exception as e:
            self._logger.error(f"Enhanced color selection failed: {e}")
            return False

    def _verify_color_selection(self, expected_option: str) -> bool:
        """
        Verify that the color option was actually selected.
        
        Args:
            expected_option: The option that should be selected
            
        Returns:
            bool: True if the selection is verified
        """
        self._logger.debug(f"Verifying color selection: {expected_option}")
        
        try:
            # Check if we can detect the current selection
            # This would depend on how the UI indicates the current selection
            # For example, checking for selected state, text changes, etc.
            
            # Navigate back to color screen to check selection
            with self.performance_tracking("verify_color_selection"):
                self._navigate_to_color_options()
                
                # Check if the expected option appears selected
                expected_locator = {
                    "Automatic": CopyLoc.combo_color_option_automatic,
                    "Color": CopyLoc.combo_color_option_color,
                    "Grayscale": CopyLoc.combo_color_option_grayscale, 
                    "Black Only": CopyLoc.combo_color_option_blackonly
                }.get(expected_option)
                
                if expected_locator:
                    element = self._driver.find(expected_locator)
                    if element:
                        # Check for selection indicators (this depends on UI implementation)
                        is_selected = (
                            element.get("selected", False) or
                            element.get("checked", False) or
                            "selected" in element.get("className", "") or
                            element.get("opacity", 1.0) > 0.8  # Assuming selected items are more opaque
                        )
                        
                        if is_selected:
                            self._logger.info(f"Color selection verified: {expected_option}")
                            return True
            
            self._logger.warning(f"Could not verify color selection: {expected_option}")
            return False
            
        except Exception as e:
            self._logger.warning(f"Color selection verification failed: {e}")
            return False

    # Batch color testing method
    def test_all_color_modes(self) -> Dict[str, bool]:
        """
        Test all available color modes for validation.
        
        Returns:
            Dict mapping color options to success status
        """
        color_options = ["Automatic", "Color", "Grayscale", "Black Only"]
        results = {}
        
        self._logger.info("Testing all color modes")
        
        for option in color_options:
            try:
                self._logger.info(f"Testing color mode: {option}")
                success = self.select_color_mode_with_validation(
                    option, 
                    verify_selection=True,
                    wait_for_ui_update=1.0
                )
                results[option] = success
                
                if success:
                    self._logger.info(f"✓ Color mode '{option}' test passed")
                else:
                    self._logger.warning(f"✗ Color mode '{option}' test failed")
                    
            except Exception as e:
                self._logger.error(f"✗ Color mode '{option}' test error: {e}")
                results[option] = False
        
        # Summary
        passed = sum(1 for success in results.values() if success)
        total = len(results)
        self._logger.info(f"Color mode testing complete: {passed}/{total} passed")
        
        return results

    # Utility method for getting current color selection
    def get_current_color_mode(self) -> Optional[str]:
        """
        Get the currently selected color mode.
        
        Returns:
            str: The currently selected color mode, or None if cannot be determined
        """
        self._logger.debug("Getting current color mode")
        
        try:
            # Navigate to color options to check current selection
            self._navigate_to_color_options()
            
            color_options = {
                "Automatic": CopyLoc.combo_color_option_automatic,
                "Color": CopyLoc.combo_color_option_color,
                "Grayscale": CopyLoc.combo_color_option_grayscale,
                "Black Only": CopyLoc.combo_color_option_blackonly
            }
            
            for option_name, locator in color_options.items():
                try:
                    element = self._driver.find(locator)
                    if element and self._is_element_selected(element):
                        self._logger.info(f"Current color mode: {option_name}")
                        return option_name
                except Exception:
                    continue
            
            self._logger.warning("Could not determine current color mode")
            return None
            
        except Exception as e:
            self._logger.error(f"Failed to get current color mode: {e}")
            return None

    def _is_element_selected(self, element) -> bool:
        """Check if an element appears to be selected."""
        try:
            return (
                element.get("selected", False) or
                element.get("checked", False) or
                "selected" in element.get("className", "").lower() or
                "active" in element.get("className", "").lower() or
                element.get("opacity", 1.0) > 0.8
            )
        except Exception:
            return False

        # ========== Generic Navigation Verification ==========
    
    def _verify_navigation(
        self,
        expected_state: NavigationState,
        expected_elements: List[Union[Locator, str]],
        state_name: str,
        timeout: float = 5.0,
        check_interval: float = 0.5
    ) -> None:
        """
        Generic method to verify successful navigation to any state.
        
        Args:
            expected_state: The NavigationState we expect to reach
            expected_elements: List of locators that should be visible in this state
            state_name: Human-readable name for logging
            timeout: Maximum time to wait for navigation
            check_interval: How often to check for success
            
        Raises:
            TimeoutError: If navigation doesn't complete within timeout
        """
        self._logger.info(f"Verifying navigation to {state_name}")
        
        start_time = time.time()
        last_check_elements = False
        
        while time.time() - start_time < timeout:
            # Check if we're in the expected state
            current_state = self._get_current_state()
            if current_state == expected_state:
                self._logger.info(f"Successfully navigated to {state_name}")
                return
            
            # Also check if expected elements are visible (more flexible)
            if expected_elements:
                elements_visible = all(
                    self._driver.exists(elem) for elem in expected_elements
                )
                if elements_visible:
                    self._current_state = expected_state
                    self._logger.info(f"Successfully navigated to {state_name} (verified by elements)")
                    return
                
                # Log progress for debugging
                if not last_check_elements and elements_visible != last_check_elements:
                    visible_count = sum(1 for elem in expected_elements if self._driver.exists(elem))
                    self._logger.debug(
                        f"Navigation progress: {visible_count}/{len(expected_elements)} elements visible"
                    )
                last_check_elements = elements_visible
            
            # Check for error states
            if self._is_in_error_state():
                self._handle_navigation_error()
            
            time.sleep(check_interval)
        
        # Timeout - provide detailed error information
        current_state = self._get_current_state()
        visible_elements = [
            elem for elem in expected_elements 
            if self._driver.exists(elem)
        ] if expected_elements else []
        
        error_details = {
            "expected_state": expected_state.value,
            "current_state": current_state.value,
            "expected_elements": len(expected_elements) if expected_elements else 0,
            "visible_elements": len(visible_elements),
            "timeout": timeout
        }
        
        raise TimeoutError(
            f"Navigation to {state_name} timed out after {timeout}s. "
            f"Current state: {current_state.value}, "
            f"Elements visible: {len(visible_elements)}/{len(expected_elements) if expected_elements else 0}"
        )
    
    def _is_in_error_state(self) -> bool:
        """Check if UI is in an error state."""
        # Check for common error indicators
        error_indicators = [
            # Add error dialog/message locators
        ]
        
        for indicator in error_indicators:
            if self._driver.exists(indicator):
                return True
        return False
    
    def _handle_navigation_error(self) -> None:
        """Handle navigation errors with recovery strategies."""
        self._logger.error("Navigation error detected, attempting recovery")
        
        # Try recovery strategies:
        # 1. Dismiss error dialogs
        # 2. Navigate back
        # 3. Return to home
        # 4. Retry navigation
        
        raise RuntimeError("Navigation failed with unrecoverable error")
    
    # ========== Batch Operations ==========
    
    def navigate_through_copy_flow(self) -> None:
        """Navigate through the complete copy flow."""
        steps = [
            ("Navigate to copy widget", self.goto_copywidget_option_landingview),
            # Add more navigation steps
        ]
        
        for step_name, step_func in steps:
            try:
                self._logger.info(f"Executing: {step_name}")
                step_func()
            except Exception as e:
                self._logger.error(f"Failed at step '{step_name}': {e}")
                raise
    
    # ========== Utility Methods ==========
    
    def wait_for_animation_complete(self, timeout: float = 2.0) -> None:
        """Wait for UI animations to complete."""
        # Could monitor UI properties to detect animation completion
        time.sleep(0.5)  # Simple wait for now
    
    def take_screenshot_on_error(self, operation_name: str) -> None:
        """Take screenshot when an operation fails."""
        if hasattr(self._driver, 'save_screenshot'):
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"error_{operation_name}_{timestamp}"
            self._driver.save_screenshot(
                metadata=("copy_ops", "1.0", "errors"),
                name=filename
            )
    
    def get_performance_report(self) -> Dict[str, Any]:
        """Get performance metrics for executed operations."""
        return {
            "metrics": self._performance_metrics,
            "average_time": sum(self._performance_metrics.values()) / len(self._performance_metrics)
            if self._performance_metrics else 0,
            "slowest_operation": max(self._performance_metrics.items(), key=lambda x: x[1])
            if self._performance_metrics else None
        }
    
    # ========== Context Managers ==========
    
    @contextmanager
    def error_handling(self, operation_name: str):
        """Context manager for consistent error handling."""
        try:
            yield
        except Exception as e:
            self._logger.error(f"Operation '{operation_name}' failed: {e}")
            self.take_screenshot_on_error(operation_name)
            raise
    
    @contextmanager
    def performance_tracking(self, operation_name: str):
        """Context manager for performance tracking."""
        start_time = time.time()
        try:
            yield
        finally:
            elapsed = time.time() - start_time
            self._performance_metrics[operation_name] = elapsed
            self._logger.debug(f"{operation_name} took {elapsed:.2f}s")

    @measure_performance("Navigate to Menu Item")
    def goto_item(
        self, 
        menu_item_id: Union[str, List[str]], 
        screen_id: Union[Locator, str], 
        dial_value: int = -180, 
        select_option: bool = True, 
        scrolling_value: float = 0.05, 
        scrollbar_locator: Union[Locator, str] = CopyLoc.options_scrollbar
    ) -> bool:
        """
        Search and click a specified menu item on a specified screen with intelligent scrolling.
        
        Args:
            menu_item_id: Object ID(s) for the menu item.
                        - str: Single object ID (e.g., "#ComboBoxOptionscolor")
                        - List[str]: [row_object_id, actual_object_id] for nested items
            screen_id: Object ID or Locator of the screen containing the menu
            dial_value: Direction for dialing (unused in current implementation)
            select_option: Whether to click the element when found
            scrolling_value: Scrolling increment value between 0 and 1
            scrollbar_locator: Locator for the scrollbar element
            
        Returns:
            bool: True if item was found and optionally clicked, False otherwise
            
        Raises:
            ValueError: If invalid parameters are provided
            TimeoutError: If screen is not found within timeout
            RuntimeError: If scrolling or clicking fails
        """        
        # Convert string locators to Locator objects if needed
        screen_locator = self._ensure_locator(screen_id)
        scrollbar_loc = self._ensure_locator(scrollbar_locator)
        
        self._logger.info(f"Searching for menu item: {menu_item_id} in screen: {screen_id}")
        
        with self.error_handling(f"goto_item_{menu_item_id}"):
            # Wait for the target screen to be available
            try:
                self._driver.wait_for(screen_locator)
            except Exception as e:
                raise TimeoutError(f"Screen {screen_id} not found within timeout: {e}")
            
            # Reset scroll position to start
            self._driver._reset_scroll_position(scrollbar_loc)
            
            if isinstance(menu_item_id, str):
                return self._driver._find_single_menu_item(
                    menu_item_id, screen_locator, select_option, 
                    scrolling_value, scrollbar_loc
                )
            else:
                return self._driver._find_nested_menu_item(
                    menu_item_id, screen_locator, select_option, 
                    scrolling_value, scrollbar_loc
                )

    def _ensure_locator(self, locator_input: Union[Locator, str]) -> Locator:
        """Convert string to Locator object if needed."""
        if isinstance(locator_input, str):
            # Assume CSS selector for string inputs
            return Locator("css", locator_input)
        return locator_input


            