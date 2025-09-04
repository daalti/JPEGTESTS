from typing import Optional, Dict, Callable, Union, List, Sequence
from contextlib import contextmanager
from functools import wraps
from enum import Enum
import time
import logging

from dunetuf.ui.new.shared.protocols.copy_ops import CopyOps
from dunetuf.ui.new.shared.decorators.measure_performance import measure_performance
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
    COPY_COLOR_LIST = "copy_color_list"

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


#@FeatureRegistry.register(Platform.DUNE, UIType.WORKFLOW, UISize.XL, Feature.COPY)
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
                CopyLoc.view_ui_main_app
            ],
            NavigationState.COPY_WIDGET_CARD: [
                CopyLoc.view_copy_widget_card_screen
            ],
            NavigationState.COPY_LANDING: [
                CopyLoc.view_copy_screen
            ],
            NavigationState.COPY_OPTIONS_LIST: [
                CopyLoc.view_copy_option_list
            ],
            NavigationState.COPY_COLOR_LIST: [
                CopyLoc.view_color_list
            ]
        }
        
        # Check states in priority order (most specific first)
        priority_order = [
            NavigationState.COPY_SETTINGS,
            NavigationState.COPY_OPTIONS_LIST,
            NavigationState.COPY_LANDING,
            NavigationState.COPY_WIDGET_CARD,
            NavigationState.HOME
        ]
        
        for state in priority_order:
            if state in state_indicators:
                locators = state_indicators[state]
                if self._driver.are_elements_visible(locators):
                    self._current_state = state
                    return state
        
        return NavigationState.UNKNOWN
        
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

    def navigate_between_views(
        self,
        target_state: NavigationState,
        target_elements: List[Locator],
        navigation_button: Locator,
        state_name: str,
        from_state: Optional[NavigationState] = None
    ) -> None:
        """
        Generic method to navigate between any two views.
        
        Args:
            target_state: The state we want to reach
            target_elements: Elements that should be visible in target state
            navigation_button: Button to click for navigation
            state_name: Human-readable name for logging
            from_state: Optional starting state to validate
            timeout: Navigation timeout
        """
        # Determine starting state
        starting_state = from_state or self._get_current_state()
        
        with self._state_transition(starting_state, target_state):
            self._logger.info(f"Navigating from {starting_state.value} to {state_name}")
            
            # Find and click navigation button
            button = self._driver.wait_for(
                navigation_button,
                condition=lambda el: el.is_enabled and el.is_visible
            )
            
            # Smart click
            click_config = ClickConfig(
                use_center=True,
                validate_after_click=True,
                retry_on_fail=True
            )
            
            if not self._driver.smart_click(button, click_config):
                raise RuntimeError(f"Failed to navigate to {state_name}")
            
            # Verify navigation
            self._verify_navigation(
                expected_state=target_state,
                expected_elements=target_elements,
                state_name=state_name
            )

    # ========= Specific Navigation Methods ==========

    @measure_performance("Go to Copy Landing Page")
    @validate_state(NavigationState.HOME)
    def goto_copy_landing_page(self) -> None:
        """
        Navigate from home view to copy landing view.
        
        Navigation path: Home View >> Copy Landing View
        
        Raises:
            TimeoutError: If navigation times out
            NavigationError: If navigation fails
        """

        button_copy_app = self._locator_combiner.descendant(
            CopyLoc.button_copy_app,
            CopyLoc.mouse_area_locator
        )

        self.navigate_between_views(NavigationState.COPY_LANDING, 
            [CopyLoc.view_copy_screen], 
            CopyLoc.button_copy_app, 
            "copy landing page", 
            from_state=NavigationState.HOME)

    @measure_performance("Go to Copy Widget Page")
    @validate_state(NavigationState.HOME)
    def goto_copy_widget_page(self) -> None:
        """
        Navigate from home view to widget copy view.

        Navigation path: Home View >> Widget Copy View

        Raises:
            TimeoutError: If navigation times out
            NavigationError: If navigation fails
        """    

        self.navigate_between_views(NavigationState.COPY_WIDGET_CARD, 
            [CopyLoc.view_copy_widget_card_screen], 
            CopyLoc.widget_button_goto_copy_app, 
            "widget copy page", 
            from_state=NavigationState.HOME)
    
    @measure_performance("Go to Copy Widget Page")
    @validate_state(NavigationState.HOME)
    def goto_copywidget_page(self) -> None:
        """
        Navigate from home view to copy widget card view.

        Navigation path: Home View >> Copy Widget Card View

        Raises:
            TimeoutError: If navigation times out
            NavigationError: If navigation fails
        """    

        self.navigate_between_views(NavigationState.COPY_LANDING, 
            [CopyLoc.view_copy_widget_card_screen], 
            CopyLoc.widget_button_goto_copy_app, 
            "copy widget option landing view", 
            from_state=NavigationState.HOME)       

    @measure_performance("Verify Navigation to Copy Landing")
    @validate_state(NavigationState.COPY_LANDING)
    def goto_option_color(self) -> None:
        """
        Navigate from copy landing view to copy options list view.
        
        Navigation path: Copy Landing View >> Copy Options List View
        
        Raises:
            TimeoutError: If navigation times out
            NavigationError: If navigation fails
        """
        self._driver.scroll_to_position(0, CopyLoc.options_scrollbar, "vertical")
        menu_item_id = [CopyLoc.row_combo_color, CopyLoc.combo_color]
        result = self.goto_item(
            menu_item_id=menu_item_id,
            screen_id=CopyLoc.view_copy_option_list,
            select_option=True,
            scrolling_value=0.1,
            scrollbar_locator=CopyLoc.options_scrollbar
        )
        assert result, "Failed to navigate to Color Mode option"
    
    @measure_performance("Go to Original Paper Type Option")
    @validate_state(NavigationState.COPY_OPTIONS_LIST)
    def goto_option_original_paper_type(self) -> None:
        """
        Navigate from copy landing view to copy options list view.
        
        Navigation path: Copy Landing View >> Copy Options List View
        
        Raises:
            TimeoutError: If navigation times out
            NavigationError: If navigation fails
        """
        menu_item_id = CopyLoc.combo_original_paper_type
        result = self.goto_item(
            menu_item_id=menu_item_id,
            screen_id=CopyLoc.view_copy_option_list,
            select_option=True,
            scrolling_value=0.1,
            scrollbar_locator=CopyLoc.options_scrollbar
        )
        assert result, "Failed to navigate to Original Paper Type option"

    @measure_performance("Go to Content Type Option")
    @validate_state(NavigationState.COPY_OPTIONS_LIST)
    def goto_option_content_type(self) -> None:
        """
        Navigate from copy landing view to copy options list view.
        
        Navigation path: Copy Landing View >> Copy Options List View
        
        Raises:
            TimeoutError: If navigation times out
            NavigationError: If navigation fails
        """
        item = self._locator_combiner.descendant(
            CopyLoc.view_copy_option_list,
            CopyLoc.row_combo_content_type
        )
        menu_item_id = self._locator_combiner.descendant(
            item,
            CopyLoc.combo_content_type
        )
        result = self.goto_item(
            menu_item_id=menu_item_id,
            screen_id=CopyLoc.view_copy_option_list,
            select_option=True,
            scrolling_value=0.1,
            scrollbar_locator=CopyLoc.options_scrollbar
        )
        assert result, "Failed to navigate to Content Type option"

    @measure_performance("Go to Resolution Option")
    @validate_state(NavigationState.COPY_OPTIONS_LIST)
    def goto_option_resolution(self) -> None:
        """
        Navigate from copy landing view to copy options list view.
        
        Navigation path: Copy Landing View >> Copy Options List View
        
        Raises:
            TimeoutError: If navigation times out
            NavigationError: If navigation fails
        """
        menu_item_id = [CopyLoc.row_combo_resolution, CopyLoc.combo_resolution]
        result = self.goto_item(
            menu_item_id=menu_item_id,
            screen_id=CopyLoc.view_copy_option_list,
            select_option=True,
            scrolling_value=0.1,
            scrollbar_locator=CopyLoc.options_scrollbar
        )
        assert result, "Failed to navigate to Resolution option"

    @measure_performance("Go to Invert Blueprints Option")
    @validate_state(NavigationState.COPY_OPTIONS_LIST)
    def goto_option_invert_blueprints(self) -> None:
        """
        Navigate from copy landing view to copy options list view.
        
        Navigation path: Copy Landing View >> Copy Options List View
        
        Raises:
            TimeoutError: If navigation times out
            NavigationError: If navigation fails
        """
        menu_item_id = CopyLoc.toggle_invert_blueprint
        result = self.goto_item(
            menu_item_id=menu_item_id,
            screen_id=CopyLoc.view_copy_option_list,
            select_option=False,
            scrolling_value=0.1,
            scrollbar_locator=CopyLoc.options_scrollbar
        )
        assert result, "Failed to navigate to Invert Blueprints option"

    @measure_performance("Go to Number of Copies Option")
    @validate_state(NavigationState.COPY_OPTIONS_LIST)
    def goto_option_number_of_copies(self) -> None:
        """
        Navigate from copy landing view to copy options list view.
        
        Navigation path: Copy Landing View >> Copy Options List View
        
        Raises:
            TimeoutError: If navigation times out
            NavigationError: If navigation fails
        """
        menu_item_id = CopyLoc.spinbox_number_of_copies
        result = self.goto_item(
            menu_item_id=menu_item_id,
            screen_id=CopyLoc.view_copy_option_list,
            select_option=False,
            scrolling_value=0.1,
            scrollbar_locator=CopyLoc.options_scrollbar
        )
        assert result, "Failed to navigate to Number of Copies option"


    @measure_performance("Select Color Mode")
    @validate_state(NavigationState.COPY_LANDING)
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
            self.goto_copy_options_list()
            
            # Select the specific color option
            self.goto_option_color()
            self._select_color_option(option)
            

    @measure_performance("Select Original Paper Type")
    @validate_state(NavigationState.COPY_LANDING)
    def select_original_paper_type(self, option: str) -> None:
        """
        Select an original paper type option in the copy settings.
        
        UI should be in copy Settings view screen.
        Navigates to original paper type screen and selects the specified paper type option.
        UI Flow: Copy Settings -> Original Paper Type -> Select Paper Type Option -> Return to Settings
        
        Args:
            option: Original paper type to select. Valid options:
                - "white": White paper
                - "photo": Photo paper
                - "translucent": Translucent paper
                - "old": Old paper
                - "oldRecycled": Old recycled paper
                - "blueprint": Blueprint paper
                - "ammonia_old_blueprint": Ammonia old blueprint paper
                - "darkBlueprints": Dark blueprint paper
                
        Raises:
            ValueError: If invalid paper type option is provided
            TimeoutError: If navigation or selection times out
            RuntimeError: If paper type selection fails
        """
        # Validate input
        valid_options = ["white", "photo", "translucent", "old", "oldRecycled", "blueprint", "ammonia_old_blueprint", "darkBlueprints"]
        if option not in valid_options:
            raise ValueError(f"Invalid paper type option '{option}'. Valid options: {valid_options}")
        
        self._logger.info(f"Selecting original paper type: {option}")
        
        with self.error_handling(f"select_original_paper_type_{option}"):
            # Navigate to original paper type options screen
            self.goto_copy_options_list()
            
            # Select the specific paper type option
            self.goto_option_original_paper_type()
            self._select_original_paper_type_option(option)

    @measure_performance("Select Content Type")
    @validate_state(NavigationState.COPY_LANDING)
    def select_content_type(self, option: str) -> None:
        """
        Select a content type option in the copy settings.
        
        UI should be in copy Settings view screen.
        Navigates to content type screen and selects the specified content type option.
        UI Flow: Copy Settings -> Content Type -> Select Content Type Option -> Return to Settings
        
        Args:
            option: Content type to select. Valid options:
                - "Mixed": Mixed content
                - "Photograph": Photograph content
                - "Text": Text content
                - "Lines": Line art content
                - "Image": Image content
                
        Raises:
            ValueError: If invalid content type option is provided
            TimeoutError: If navigation or selection times out
            RuntimeError: If content type selection fails
        """
        # Validate input
        valid_options = ["Mixed", "Photograph", "Text", "Lines", "Image"]
        if option not in valid_options:
            raise ValueError(f"Invalid content type option '{option}'. Valid options: {valid_options}")
        
        self._logger.info(f"Selecting content type: {option}")
        
        with self.error_handling(f"select_content_type_{option}"):
            # Navigate to content type options screen
            self.goto_copy_options_list()

            self.goto_option_content_type()
            # Select the specific content type option
            self._select_content_type_option(option)

    @measure_performance("Select Content Type")
    @validate_state(NavigationState.COPY_LANDING)
    def select_resolution(self, option: str) -> None:
        """
        Select a resolution option in the copy settings.
        
        UI should be in copy Settings view screen.
        Navigates to resolution screen and selects the specified resolution option.
        UI Flow: Copy Settings -> Resolution -> Select Resolution Option -> Return to Settings
        
        Args:
            option: Resolution to select. Valid options:
                - "200dpi": 200 DPI
                - "300dpi": 300 DPI
                - "600dpi": 600 DPI
                
        Raises:
            ValueError: If invalid resolution option is provided
            TimeoutError: If navigation or selection times out
            RuntimeError: If resolution selection fails
        """
        # Validate input
        valid_options = ["200dpi", "300dpi", "600dpi"]
        if option not in valid_options:
            raise ValueError(f"Invalid resolution option '{option}'. Valid options: {valid_options}")
        
        self._logger.info(f"Selecting resolution: {option}")
        
        with self.error_handling(f"select_resolution_{option}"):
            # Navigate to resolution options screen
            self.goto_copy_options_list()

            self.goto_option_resolution()
            # Select the specific resolution option
            self._select_resolution_option(option)

    @measure_performance("Select Number of Copies")
    @validate_state(NavigationState.COPY_LANDING)
    def select_number_of_copies(self, count: int) -> None:
        """
        Select the number of copies in the copy settings.
        
        UI should be in copy Settings view screen.
        Navigates to number of copies option and sets the specified count.
        UI Flow: Copy Settings -> Number of Copies -> Set Count -> Return to Settings
        
        Args:
            count (int): Number of copies to set (1-99)
                
        Raises:
            ValueError: If count is out of valid range
            TimeoutError: If navigation or selection times out
            RuntimeError: If setting number of copies fails
        """
        # Validate input
        if not (1 <= count <= 99):
            raise ValueError("Number of copies must be between 1 and 99")
        
        self._logger.info(f"Setting number of copies to: {count}")
        
        with self.error_handling(f"select_number_of_copies_{count}"):
            # Navigate to number of copies option
            self.goto_copy_options_list()

            self.goto_option_number_of_copies()
            # Set the number of copies
            self._set_number_of_copies(count)

    @measure_performance("Select Content Type")
    @validate_state(NavigationState.COPY_LANDING)
    def toggle_invert_blueprints(self, enable: bool) -> None:
        """
        Enable or disable the invert blueprints setting for copying.
        
        UI should be in copy Settings view screen.
        Navigates to invert blueprints option and toggles it.
        UI Flow: Copy Settings -> Invert Blueprints -> Toggle Option -> Return to Settings
        
        Args:
            enable (bool): True to enable invert blueprints, False to disable.
                
        Raises:
            TimeoutError: If navigation or selection times out
            RuntimeError: If toggle action fails
        """
        
        self._logger.info(f"Setting invert blueprints to: {'Enable' if enable else 'Disable'}")
        
        with self.error_handling(f"toggle_invert_blueprints_{'enable' if enable else 'disable'}"):
            # Navigate to invert blueprints option
            self.goto_copy_options_list()

            self.goto_option_invert_blueprints()
            # Toggle the invert blueprints option
            self._toggle_invert_blueprint_option(enable)
            
            

    @validate_state(NavigationState.COPY_OPTIONS_LIST)
    def goto_copy_options_list(self) -> None:
        """Public method to navigate to color options screen."""

        self.navigate_between_views(NavigationState.COPY_OPTIONS_LIST, 
            [CopyLoc.view_copy_screen], 
            self._locator_combiner.descendant(
                CopyLoc.view_copy_screen,
                CopyLoc.button_copy_more_options
            ), 
            "copy options list view", 
            from_state=NavigationState.COPY_LANDING)
        


    def _navigate_to_color_options(self) -> None:
        """Navigate from copy settings to color options screen."""
        self._logger.info("Navigating to color options screen")
        
        with self._state_transition(NavigationState.COPY_OPTIONS_LIST, NavigationState.COPY_COLOR_LIST):
            # Use the existing goto_copy_option_color_screen method
            #self.goto_option_color_screen()
            
            # Wait for color options to be available
            self._driver.wait_for(
                CopyLoc.view_color_list,
                condition=lambda el: el.is_visible
            )
            
            # Allow UI to settle after navigation
            time.sleep(1.0)
            
            self._logger.info("Successfully navigated to color options screen")

    def  _select_color_option(self, option: str) -> None:
        """
        Select the specified color option from the color list.
        
        Args:
            option: The color option to select
        """
        self._logger.info(f"Selecting color option: {option}")
        # First, click to open the color options list if needed
        try:                            
            click_config = ClickConfig(
                use_center=True,
                validate_after_click=True,
                retry_on_fail=True,
                max_retries=3,
                wait_after_click=0.5
            )
            menu_item_id = self._locator_combiner.descendant(
                self._locator_combiner.descendant(
                    CopyLoc.view_copy_option_list,
                    CopyLoc.row_combo_color
                ),
                CopyLoc.combo_color
            )
            element = self._driver.wait_for(
                menu_item_id,
                condition=lambda el: el.is_visible
            )
            # Perform the click using smart click
            self._logger.info(f"Clicking color option to open list")
            success = self._driver.smart_click(element, click_config)
        
            if not success:
                raise RuntimeError(f"Failed to click color option list")
                        
            self._logger.info(f"Successfully selected color option list")
        except Exception as e:
            self._logger.error(f"Failed to select color option list: {e}")
            raise RuntimeError(f"Color option list selection failed: {e}")

        # Wait for the color options list to be visible
        self._driver.wait_for(
            CopyLoc.view_color_list,
            condition=lambda el: el.is_visible
        )
        # Define color option locators mapping
        color_option_locators = {
            "Automatic": CopyLoc.opt_color_auto,
            "Color": CopyLoc.opt_color_color, 
            "Grayscale": CopyLoc.opt_color_grayscale,
            "Black Only": CopyLoc.opt_color_blackonly
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
                        
            self._logger.info(f"Successfully selected color option: {option}")
            
        except Exception as e:
            self._logger.error(f"Failed to select color option '{option}': {e}")
            raise RuntimeError(f"Color option selection failed for '{option}': {e}")
        

    def  _select_original_paper_type_option(self, option: str) -> None:
        """
        Select the specified original paper type option from the original paper type list.
        
        Args:
            option: The original paper type option to select
        """
        # Define original paper type option locators mapping
        original_paper_option_locators = {
            "white": CopyLoc.opt_original_paper_white,
            "photo": CopyLoc.opt_original_paper_photo,
            "translucent": CopyLoc.opt_original_paper_translucent,
            "old": CopyLoc.opt_original_paper_old_recycled,
            "oldRecycled": CopyLoc.opt_original_paper_blueprints, #TODO: Check this
            "blueprint": CopyLoc.opt_original_paper_blueprints,
            "ammonia_old_blueprint": CopyLoc.opt_original_paper_blueprints, #TODO: Check this
            "darkBlueprints": CopyLoc.opt_original_paper_dark_blueprints
        }
        self._driver.wait_for(
            CopyLoc.view_original_paper_type_list,
            condition=lambda el: el.is_visible
        )
        # Get the locator for the requested option
        option_locator = original_paper_option_locators.get(option)
        if not option_locator:
            raise ValueError(f"No locator defined for original paper type option: {option}")        

        self._logger.info(f"Selecting original paper type option: {option}")
        # First, click to open the original paper type options list if needed  
        try:
            self._driver.scroll_to_position(0, CopyLoc.view_paper_selection_scrollbar, "vertical")
            menu_item_id = option_locator
            result = self.goto_item(
                menu_item_id=menu_item_id,
                screen_id=CopyLoc.view_original_paper_type_list,
                select_option=True,
                scrolling_value=0.1,
                scrollbar_locator=CopyLoc.view_paper_selection_scrollbar
            )     
            assert result, f"Failed to navigate to Original Paper Type option '{option}'"
            self._logger.info(f"Successfully selected original paper type option list: {option}") 

        except Exception as e:
            self._logger.error(f"Failed to select original paper type option '{option}': {e}")
            raise RuntimeError(f"Original paper type option selection failed for '{option}': {e}")
        
    def  _select_content_type_option(self, option: str) -> None:
        """
        Select the specified content type option from the content type list.
        
        Args:
            option: The content type option to select
        """
        # Define content type option locators mapping
        content_type_option_locators = {
            "Mixed": CopyLoc.opt_content_mixed,
            "Photograph": CopyLoc.opt_content_photograph,
            "Text": CopyLoc.opt_content_text,
            "Lines": CopyLoc.opt_content_lines,
            "Image": CopyLoc.opt_content_image
        }

        self._driver.wait_for(
            CopyLoc.view_content_type_list,
            condition=lambda el: el.is_visible
        )

        # Get the locator for the requested option
        option_locator = content_type_option_locators.get(option)
        if not option_locator:
            raise ValueError(f"No locator defined for content type option: {option}")        

        self._logger.info(f"Selecting content type option: {option}")
        # First, click to open the content type options list if needed  
        try:
            self._driver.scroll_to_position(0, CopyLoc.standard_sizes_scrollbar, "vertical")
            menu_item_id = option_locator
            result = self.goto_item(
                menu_item_id=menu_item_id,
                screen_id=CopyLoc.view_content_type_list,
                select_option=True,
                scrolling_value=0.1,
                scrollbar_locator=CopyLoc.standard_sizes_scrollbar
            )     
            assert result, f"Failed to navigate to Content Type option '{option}'"
            self._logger.info(f"Successfully selected content type option list: {option}") 

        except Exception as e:
            self._logger.error(f"Failed to select content type option '{option}': {e}")
            raise RuntimeError(f"Content type option selection failed for '{option}': {e}")
        
    def  _select_resolution_option(self, option: str) -> None:
        """
        Select the specified resolution option from the resolution list.

        Args:
            option: The resolution option to select
        """

        # Define resolution option locators mapping
        resolution_option_locators = {
            "200dpi": CopyLoc.opt_resolution_200,
            "300dpi": CopyLoc.opt_resolution_300,
            "600dpi": CopyLoc.opt_resolution_600
        }

        # Get the locator for the requested option
        option_locator = resolution_option_locators.get(option)
        if not option_locator:
            raise ValueError(f"No locator defined for resolution option: {option}")        


        self._driver.wait_for(
            CopyLoc.view_resolution_list,
            condition=lambda el: el.is_visible
        )
        self._logger.info(f"Selecting resolution option: {option}")
        # First, click to open the resolution options list if needed  
        try:
            self._driver.scroll_to_position(0, CopyLoc.standard_sizes_scrollbar, "vertical")
            menu_item_id = option_locator
            result = self.goto_item(
                menu_item_id=menu_item_id,
                screen_id=CopyLoc.view_resolution_list,
                select_option=True,
                scrolling_value=0.1,
                scrollbar_locator=CopyLoc.standard_sizes_scrollbar
            )     
            assert result, f"Failed to navigate to Resolution option '{option}'"
            self._logger.info(f"Successfully selected resolution option list: {option}") 

        except Exception as e:
            self._logger.error(f"Failed to select resolution option '{option}': {e}")
            raise RuntimeError(f"Resolution option selection failed for '{option}': {e}")

    def _toggle_invert_blueprint_option(self, enable: bool) -> None:
        """
        Toggle the invert blueprints option.

        Args:
            enable (bool): True to enable, False to disable
        """
        self._logger.info(f"Toggling invert blueprints to: {'Enable' if enable else 'Disable'}")
        try:
            toggle_locator = CopyLoc.toggle_invert_blueprint
            toggle_element = self._driver.wait_for(
                toggle_locator,
                condition=lambda el: el.is_visible and el.is_enabled
            )
            
            # Determine current state
            if enable == toggle_element["checked"]:
                logging.info("Invert blueprints option already in desired state")
                return            

            click_config = ClickConfig(
                use_center=True,
                validate_after_click=True,
                retry_on_fail=True,
                max_retries=3,
                wait_after_click=0.5
            )
            
            self._logger.info(f"Clicking toggle to {'enable' if enable else 'disable'}")
            success = self._driver.smart_click(toggle_element, click_config)
            
            if not success:
                raise RuntimeError("Failed to click invert blueprints toggle")
            
            self._logger.info("Successfully toggled invert blueprints option")

                
        except Exception as e:
            self._logger.error(f"Failed to toggle invert blueprints option: {e}")
            raise RuntimeError(f"Toggling invert blueprints option failed: {e}")

    def _set_number_of_copies(self, count: int) -> None:
        """
        Set the number of copies using the spinbox control.

        Args:
            count (int): Number of copies to set (1-99)
        """
        self._logger.info(f"Setting number of copies to: {count}")
        try:
            spinbox_locator = CopyLoc.spinbox_number_of_copies
            spinbox_element = self._driver.wait_for(
                spinbox_locator,
                condition=lambda el: el.is_visible and el.is_enabled
            )
            spinbox_element['value'] = count  # Update the value attribute            
            self._logger.info("Successfully set number of copies")
                
        except Exception as e:
            self._logger.error(f"Failed to set number of copies: {e}")
            raise RuntimeError(f"Setting number of copies failed: {e}")


    @measure_performance("Go Back to Copy Landing")
    @validate_state(NavigationState.COPY_OPTIONS_LIST)
    def go_back_to_copy_landing(self) -> None:
        """
        Navigate back from copy options list view to copy landing view.
        
        Navigation path: Copy Options List View >> Copy Landing View
        
        This method is used when you need to return from the detailed options
        list to the main copy landing page, typically after configuring options
        or when the user wants to go back to the previous screen.
        
        Raises:
            TimeoutError: If navigation times out
            NavigationError: If navigation fails
            RuntimeError: If back button is not available
        """
        self._logger.info("Navigating back from Copy Options List to Copy Landing")

        close_button = self._locator_combiner.descendant(
            CopyLoc.view_copy_option_list,
            CopyLoc.button_close
        )

        self.navigate_between_views(
            target_state=NavigationState.COPY_LANDING,
            target_elements=[CopyLoc.view_copy_screen],
            navigation_button=close_button,
            state_name="copy landing page (back navigation)",
            from_state=NavigationState.COPY_OPTIONS_LIST,
        )
        
        self._logger.info("Successfully navigated back to Copy Landing view")

    @measure_performance("Click Start Button")
    @validate_state(NavigationState.COPY_LANDING)
    def click_start(self) -> None:
        """Click the Start button to initiate copying."""
        self._logger.info("Clicking Start button to initiate copy")
        
        try:
            start_button = self._driver.wait_for(
                CopyLoc.button_start_copy,
                condition=lambda el: el.is_visible and el.is_enabled
            )
            
            click_config = ClickConfig(
                use_center=True,
                validate_after_click=True,
                retry_on_fail=True
            )
            
            if not self._driver.smart_click(start_button, click_config):
                raise RuntimeError("Failed to click Start button")
            
            self._logger.info("Successfully clicked Start button")
            
        except Exception as e:
            self._logger.error(f"Failed to click Start button: {e}")
            raise RuntimeError(f"Clicking Start button failed: {e}")
        
    # ========== Generic Navigation Verification ==========
    
    def _verify_navigation(
        self,
        expected_state: NavigationState,
        expected_elements: Sequence[Union[Locator, str]],
        state_name: str,
        timeout: float = 10.0,
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
    
    # ========== Utility Methods ==========
    
   
    def take_screenshot_on_error(self, operation_name: str) -> None:
        """Take screenshot when an operation fails."""
        if hasattr(self._driver, 'save_screenshot'):
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"error_{operation_name}_{timestamp}"
            self._driver.save_screenshot(
                metadata=("copy_ops", "1.0", "errors"),
                name=filename
            )
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
        menu_item_id: Union[Locator, List[Locator]], 
        screen_id: Locator, 
        dial_value: int = -180, 
        select_option: bool = True, 
        scrolling_value: float = 0.05, 
        scrollbar_locator: Locator = CopyLoc.options_scrollbar
    ) -> bool:
        """
        Search and click a specified menu item on a specified screen with intelligent scrolling.
        
        Args:
            menu_item_id: Locator(s) for the menu item.
                        - Locator: Single locator object
                        - List[Locator]: [row_locator, item_locator] for nested items
            screen_id: Locator of the screen containing the menu
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
        
        if not isinstance(screen_id, Locator):
            raise ValueError("screen_id must be a Locator object")
        
        if not isinstance(scrollbar_locator, Locator):
            raise ValueError("scrollbar_locator must be a Locator object")
        
        self._logger.info(f"Searching for menu item: {menu_item_id} in screen: {screen_id}")
        
        with self.error_handling(f"goto_item_{menu_item_id}"):
            # Wait for the target screen to be available
            try:
                self._driver.wait_for(screen_id, timeout=10.0)
            except Exception as e:
                raise TimeoutError(f"Screen {screen_id} not found within timeout: {e}")
            
            # Reset scroll position to start
            self._driver._reset_scroll_position(scrollbar_locator)
            
            if isinstance(menu_item_id, Locator):
                return self._driver._find_locator_menu_item(
                    menu_item_id, screen_id, select_option, 
                    scrolling_value, scrollbar_locator
                )
            else:  # List[Locator]
                return self._driver._find_nested_locator_menu_item(
                    menu_item_id, screen_id, select_option, 
                    scrolling_value, scrollbar_locator
                )