"""
Navigation and Selection Handler Module
Common navigation and option selection functionality for UI operations
"""

from typing import Union, List, Optional, Any, Dict
import logging
import time

from dunetuf.ui.new.shared.config_generator import ConfigGenerator
from contextlib import contextmanager
from dunetuf.ui.new.shared.state_machine import StateMachine
from dunetuf.ui.new.shared.driver import ClickConfig
from dunetuf.ui.new.shared.option_handler import GenericOptionHandler
from dunetuf.ui.new.shared.decorators.measure_performance import measure_performance
from dunetuf.ui.new.shared.locator_base import Locator
from dunetuf.ui.new.shared.enums import Feature
from .locator_resolver import LocatorResolver
from .global_state_manager import get_global_state_manager


class NavigationHandler:
    """Handles common navigation and selection operations."""
    
    def __init__(
        self,
        driver: Any,
        logger: Optional[logging.Logger] = None,
        locator_provider: Any = None,
        state_machine: Optional[StateMachine] = None,
        config_generator: Optional[ConfigGenerator] = None,
        option_handler: Optional[GenericOptionHandler] = None,
        option_configs: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        performance_metrics: Optional[Dict[str, List[float]]] = None,
        feature: Optional[Feature] = None 
    ):
        """Initialize with driver, logger, and state machine.
        
        Args:
            driver: UI driver for interactions
            logger: Logger instance
            locator_provider: Locator provider instance
            state_machine: State machine for navigation
            config_generator: Configuration generator instance
            option_handler: Option handler instance
            option_configs: Dictionary of option configurations
            metadata: Additional metadata dictionary
            performance_metrics: Dictionary to track performance metrics (lists of values)
        """
        self._state_machine = state_machine
        self._config_generator = config_generator
        self._option_handler = option_handler
        self._option_configs = option_configs or {}
        self._metadata = metadata or {}
        self._driver = driver
        self._locator_provider = locator_provider
        self._logger = logger or logging.getLogger(__name__)
        self._performance_metrics = performance_metrics or {}

        self._locator_resolver = LocatorResolver(
            locator_provider=locator_provider,
            config_generator=config_generator
        )
        self._feature = feature
        self._global_state_manager = get_global_state_manager()

        self._is_feature_active = False
        
        # Register with global state manager if feature is specified
        if feature and state_machine:
            self._global_state_manager.register_feature(
                feature=feature,
                state_machine=state_machine,
                config_generator=config_generator,
                navigation_handler=self,
                metadata=metadata
            )
            
            if self._state_machine:
                if self._state_machine.current_state == "HOME":
                    feature = Feature.HOME

            self._global_state_manager.set_current_feature(feature)

    def _ensure_feature_active(self) -> None:
        """
        Ensure this feature is set as current in global state manager.
        Auto-activates on first operation.
        """
        if self._feature:
            # Check if current state is HOME and update feature accordingly
            if self._state_machine and self._state_machine.current_state == "HOME":
                feature = Feature.HOME
            else:
                feature = self._feature
            
            current_feature = self._global_state_manager.get_current_feature()
            
            # Only update if we're not already the current feature
            if current_feature != feature:
                self._global_state_manager.set_current_feature(feature)
                self._is_feature_active = True
                self._logger.info(f"Activated feature: {feature.value} (was: {current_feature})")
            elif not self._is_feature_active:
                self._is_feature_active = True
                self._logger.debug(f"Feature {feature.value} already active")
    
    @measure_performance("Navigate to State")
    def navigate_to(self, target_state: str) -> None:
        """
        Navigate to target state using state machine.
        
        Args:
            target_state: Name of target state
            
        Raises:
            ValueError: If target state doesn't exist
            RuntimeError: If navigation fails
        """
        # Auto-activate feature on first navigation
        self._ensure_feature_active()

        if self._state_machine is None:
            raise RuntimeError("Cannot navigate: state machine is not initialized")
        
        if target_state not in self._state_machine._states:
            raise ValueError(f"Unknown state: {target_state}")
        
        current_state = self._state_machine.current_state
        
        if current_state is None:
            raise RuntimeError("Cannot navigate: current state is unknown")
        
        if current_state == target_state:
            self._logger.info(f"Already in state: {target_state}")
            return
        
        self._logger.info(f"Navigating from {current_state} to {target_state}")
        
        # Record start time for performance tracking
        self._transition_start_time = time.time()
        
        try:
            # Check if direct transition exists
            if self._state_machine.can_transition(target_state):
                self._execute_transition(current_state, target_state)
            else:
                # Find path using graph (if implemented)
                self._logger.warning(f"No direct transition from {current_state} to {target_state}")
                # Could implement pathfinding here
                raise RuntimeError(f"Cannot navigate from {current_state} to {target_state}")
            
        except Exception as e:
            self._logger.error(f"Navigation failed: {e}")
            self._take_screenshot_on_error(f"nav_{current_state}_to_{target_state}")
            raise

    def navigate_to_global_home(self) -> bool:
        """
        Navigate to global HOME using the global state manager.
        
        Returns:
            bool: True if navigation successful
        """
        # Auto-activate feature before global navigation
        self._ensure_feature_active()

        try:
            return self._global_state_manager.navigate_to_home()
        except Exception as e:
            self._logger.error(f"Global home navigation failed: {e}")
            return False
    
    def get_global_status(self) -> Dict[str, Any]:
        """Get global status information."""
        return self._global_state_manager.export_status_report()
    
    @measure_performance("Select Option")
    def select_option(self, option_name: str, value: Any) -> None:
        """
        Select an option value using configuration.
        
        Args:
            option_name: Name of option to select
            value: Value to set
            
        Raises:
            ValueError: If option doesn't exist
            ValidationError: If value is invalid
            RuntimeError: If option handler is not initialized
        """
        # Auto-activate feature on first option selection
        self._ensure_feature_active()

        if self._option_handler is None:
            raise RuntimeError("Cannot select option: option handler is not initialized")
        
        if option_name not in self._option_configs:
            raise ValueError(f"Unknown option: {option_name}")
        
        config = self._option_configs[option_name]
        
        # Ensure we're in the right state for this option
        #self._ensure_option_accessible(config)
        
        # Select the option
        self._option_handler.select_option(config, value)

        # Store current state before selection
        current_state = None
        if self._state_machine:
            current_state = self._state_machine.current_state

        # Handle automatic state transitions after combo selections
        if config.option_type.value == "combo" and current_state:
            self._handle_post_combo_transition(current_state)
        
        # Record metric
        self._record_metric(f"option_select_{option_name}", 1)
       
    def navigate_back(self, back_button_locator: Any) -> bool:
        """
        Navigate back using a back button.
        
        Args:
            back_button_locator: Locator for the back button
            
        Returns:
            bool: True if navigation successful
        """
        try:
            self._logger.debug("Navigating back")
            self._driver.click(back_button_locator)
            time.sleep(0.5)  # Allow UI to transition
            return True
        except Exception as e:
            self._logger.error(f"Failed to navigate back: {e}")
            return False
    
    def wait_for_screen(
        self,
        screen_locators: Union[List[Any], Any],
        timeout: float = 10.0
    ) -> bool:
        """
        Wait for a screen to be ready.
        
        Args:
            screen_locators: Locator(s) that identify the screen
            timeout: Maximum wait time
            
        Returns:
            bool: True if screen is ready
        """
        if not isinstance(screen_locators, list):
            screen_locators = [screen_locators]
        
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            for locator in screen_locators:
                try:
                    if self._driver.exists(locator):
                        element = self._driver.find(locator)
                        if element.is_visible:
                            self._logger.debug("Screen is ready")
                            return True
                except Exception:
                    pass
            
            time.sleep(0.5)
        
        self._logger.warning(f"Screen not ready after {timeout}s")
        return False

    def _execute_transition(self, from_state: str, to_state: str) -> None:
        """Execute a state transition."""
        if not self._state_machine:
            raise RuntimeError("State machine not initialized")
        
        # Get transition configuration
        transition = self._state_machine.get_transition(from_state, to_state)
        if not transition:
            raise ValueError(f"No transition found from {from_state} to {to_state}")
        
        try:
            # Check if this is an auto transition
            if transition.metadata.get("auto_transition"):
                self._logger.info(f"Auto transition from {from_state} to {to_state}")
                # Wait for animation duration
                animation_duration = transition.metadata.get("animation_duration", 0.2)
                if animation_duration > 0:
                    time.sleep(animation_duration)
                return
            
            # Get button to click
            button_ref = transition.metadata.get("button")
            if not button_ref:
                raise ValueError(f"No button specified for transition from {from_state} to {to_state}")
            
            # Resolve button locator
            button_locator = self._locator_resolver.resolve(button_ref)
            
            # Handle scrolling if required BEFORE clicking
            scrolling_config = transition.metadata.get("scrolling")
            if scrolling_config and scrolling_config.get("required", False):
                increment = scrolling_config.get("increment", 0.1)
                scrollbar = scrolling_config.get("scrollbar")
                
                # Resolve scrollbar locator with null check
                scrollbar_locator = self._locator_resolver.resolve(scrollbar)
                
                direction = scrolling_config.get("direction", "vertical")
                self._driver.scroll_to_position(0, scrollbar_locator, direction)
                
                self._goto_item(menu_item_id=button_locator, select_option=True, scrolling_value=increment, scrollbar_locator=scrollbar_locator) #type: ignore
            else:
                # Click the navigation button
                self._click_navigation_button(button_locator)
            
            # Wait for animation
            animation_duration = transition.metadata.get("animation_duration", 0.5)
            if animation_duration > 0:
                time.sleep(animation_duration)

            # Wait for target screen to be stable
            self._wait_for_target_screen_stable(to_state, transition)

            # Update state machine
            self._state_machine.transition_to(to_state)
                
        except Exception as e:
            self._logger.error(f"Failed to execute transition from {from_state} to {to_state}: {e}")
            self._take_screenshot_on_error(f"transition_{from_state}_to_{to_state}")
            raise       

    #TODO: ASK WHY IS NOT WORKING
    def _wait_for_target_screen_stable(self, target_state: str, transition) -> None:
        """Wait for target screen to be visible and stable after transition."""
        try:
            # Option 1: Use target screen characteristic elements from metadata
            target_elements = transition.metadata.get("target_elements")
            if target_elements:
                # If specific elements are defined in the transition
                for element_ref in target_elements:
                    try:
                        if (self._config_generator is not None and 
                            hasattr(self._config_generator, '_locator_resolver') and 
                            self._config_generator._locator_resolver is not None):
                            element_locator = self._config_generator._locator_resolver.resolve(element_ref)
                        else:
                            element_locator = getattr(self._locator_provider, element_ref)
                        
                        self._logger.debug(f"Waiting for target screen element to be stable: {element_ref}")
                        self._driver.wait_for_visible_stable(
                            element_locator,
                            min_stable_ms=300,  # 300ms of stability
                            timeout=10.0
                        )
                        self._logger.debug(f"Target screen element is stable: {element_ref}")
                        return  # If we find one, we're ready
                        
                    except Exception as e:
                        self._logger.debug(f"Could not wait for element {element_ref}: {e}")
                        continue
            
            # Option 2: Use target state elements from state machine
            target_state_obj = self._state_machine.get_state_object(target_state) # type: ignore
            if target_state_obj and target_state_obj.metadata.get("view_elements"):
                view_elements = target_state_obj.metadata["view_elements"]
                all_elements_stable = True
                
                for element_ref in view_elements:
                    try:
                        element_locator = getattr(self._locator_provider, element_ref)
                        
                        self._logger.debug(f"Waiting for state view element to be stable: {element_ref}")
                        self._driver.wait_for_visible_stable(
                            element_locator,
                            min_stable_ms=300,
                            timeout=10.0
                        )
                        self._logger.debug(f"State view element is stable: {element_ref}")
                        
                    except Exception as e:
                        self._logger.debug(f"Could not wait for state element {element_ref}: {e}")
                        all_elements_stable = False
                        break
                
                if all_elements_stable:
                    self._logger.debug("All state view elements are stable")
                    return
                else:
                    self._logger.warning(f"Not all view elements are stable for state {target_state}")
            
            # Option 3: Fallback - wait additional time if no specific elements are available
            self._logger.warning(f"No specific elements defined for state {target_state}, using fallback wait")
            #time.sleep(1.0)  # Additional wait as fallback
            
        except Exception as e:
            self._logger.warning(f"Error waiting for target screen stability: {e}")
            # Don't fail the transition for this, just log warning

    def _click_navigation_button(self, button_locator: Any) -> None:
        logging.info(f"Clicking navigation button: {button_locator}")
        """Click a navigation button."""
        button = self._driver.wait_for(
            button_locator,
            condition=lambda el: el.is_enabled and el.is_visible
        )
        
        click_config = ClickConfig(
            use_center=True,
            validate_after_click=True,
            retry_on_fail=True
        )
        
        if not self._driver.smart_click(button, click_config):
            raise RuntimeError(f"Failed to click navigation button")

    def _take_screenshot_on_error(self, operation_name: str) -> None:
        """Take screenshot when an operation fails."""
        if hasattr(self._driver, 'save_screenshot'):
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"error_{operation_name}_{timestamp}"
            self._driver.save_screenshot(
                metadata=("copy_ops", self._metadata['version'], "errors"),
                name=filename
            )

    def _record_metric(self, metric_name: str, value: float) -> None:
        """Record a performance metric."""
        if metric_name not in self._performance_metrics:
            self._performance_metrics[metric_name] = []
        self._performance_metrics[metric_name].append(value)

    def _handle_post_combo_transition(self, previous_state: str) -> None:
        """Handle automatic transitions after combo box selections."""
        if not self._state_machine:
            return
            
        # Look for auto transitions from the previous state
        for transition_key, transition in self._state_machine._transitions.items():
            from_state, to_state = transition_key
            
            if (from_state == previous_state and 
                transition.metadata.get("auto_transition") == True):
                
                self._logger.info(f"Handling auto transition from {from_state} to {to_state} after combo selection")
                
                # Wait for animation
                animation_duration = transition.metadata.get("animation_duration", 0.2)
                if animation_duration > 0:
                    time.sleep(animation_duration)
                
                # Update state machine
                self._state_machine.transition_to(to_state)
                
                # Wait for target screen
                self._wait_for_target_screen_stable(to_state, transition)
                break

    def _goto_item(
        self, 
        menu_item_id: Union[Locator, List[Locator]], 
        scrollbar_locator: Locator,
        dial_value: int = -180, 
        select_option: bool = True, 
        scrolling_value: float = 0.05
    ) -> bool:
        """
        Search and click a specified menu item on a specified screen with intelligent scrolling.
        
        Args:
            menu_item_id: Locator(s) for the menu item.
                        - Locator: Single locator object
                        - List[Locator]: [row_locator, item_locator] for nested items
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
        if not isinstance(menu_item_id, (Locator, list)):
            raise ValueError("menu_item_id must be a Locator or list of Locators")
        
        if isinstance(menu_item_id, list):
            if len(menu_item_id) != 2:
                raise ValueError("menu_item_id list must contain exactly 2 Locator objects [row_locator, item_locator]")
            if not all(isinstance(loc, Locator) for loc in menu_item_id):
                raise ValueError("All elements in menu_item_id list must be Locator objects")
        
        if not isinstance(scrollbar_locator, Locator):
            raise ValueError("scrollbar_locator must be a Locator object")
        
        with self.error_handling(f"goto_item_{menu_item_id}"):           
            # Reset scroll position to start
            self._driver._reset_scroll_position(scrollbar_locator)
            
            if isinstance(menu_item_id, Locator):
                return self._driver._find_locator_menu_item(
                    menu_item_id, select_option=select_option, 
                    scrolling_value=scrolling_value, scrollbar_locator=scrollbar_locator
                )
            else:  # List[Locator]
                return self._driver._find_nested_locator_menu_item(
                    menu_item_id, select_option, 
                    scrolling_value, scrollbar_locator
                )

    def force_state_transition(self, target_state: str, update_global: bool = True, timeout: float = 1.0 ) -> None:
        """
        Force state transition without executing any UI actions.
        Useful for synchronizing state machine with actual UI state.
        
        Args:
            target_state: Target state to transition to
            update_global: Whether to update global state manager
            
        Raises:
            ValueError: If target state doesn't exist
        """
        if self._state_machine is None:
            raise RuntimeError("Cannot force transition: state machine is not initialized")
        
        if target_state not in self._state_machine._states:
            raise ValueError(f"Unknown state: {target_state}")
        
        current_state = self._state_machine.current_state
        
        self._logger.info(f"FORCE TRANSITION: {current_state} -> {target_state} (no UI actions)")
        
        try:
            # Update state machine directly without UI actions
            self._state_machine._current_state = target_state
            
            # Update feature context if global state management is active
            if update_global and self._feature:
                self._ensure_feature_active()
                
                # Update the feature context directly
                context = self._global_state_manager._feature_contexts.get(self._feature)
                if context:
                    context.current_state = target_state
                    self._global_state_manager._add_to_history(f"FORCE_TRANSITION:{self._feature.value}:{target_state}")
            
            # Trigger state change listeners
            if hasattr(self._state_machine, '_listeners'):
                for listener in self._state_machine._listeners:
                    try:
                        listener(current_state or "UNKNOWN", target_state)
                    except Exception as e:
                        self._logger.warning(f"State listener failed: {e}")
            
            time.sleep(timeout)  # Allow brief pause for stability
            self._logger.info(f"Successfully forced transition to: {target_state}")
            
        except Exception as e:
            self._logger.error(f"Failed to force transition to {target_state}: {e}")
            raise
    
    def sync_state_with_ui(self, detected_state: str) -> None:
        """
        Synchronize state machine with actual UI state.
        Use when UI state detection determines actual current state.
        
        Args:
            detected_state: The state detected from UI elements
        """
        self.force_state_transition(detected_state, update_global=True)
        self._logger.info(f"Synchronized state machine with UI state: {detected_state}")

    @contextmanager
    def error_handling(self, operation_name: str):
        """Context manager for consistent error handling."""
        try:
            yield
        except Exception as e:
            self._logger.error(f"Operation '{operation_name}' failed: {e}")
            self.take_screenshot_on_error(operation_name)
            raise

    def take_screenshot_on_error(self, operation_name: str) -> None:
        """Take screenshot when an operation fails."""
        if hasattr(self._driver, 'save_screenshot'):
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"error_{operation_name}_{timestamp}"
            self._driver.save_screenshot(
                metadata=("copy_ops", "1.0", "errors"),
                name=filename
            )

    #TODO: IS NECESSARY?
    def get_current_feature_status(self) -> Dict[str, Any]:
        """Get status of this navigation handler's feature."""
        return {
            "feature": self._feature.value if self._feature else None,
            "is_active": self._is_feature_active,
            "is_global_current": self._global_state_manager.get_current_feature() == self._feature,
            "can_activate": self._feature is not None
        }