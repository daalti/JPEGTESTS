"""
Common Copy Operations with Configuration-Based Architecture
Base implementation using shared components for all sizes
"""

from pathlib import Path
from typing import Dict, Any, Optional, List
import logging
from functools import wraps
import time

# Import shared components
from dunetuf.ui.new.shared.option_handler import GenericOptionHandler, OptionConfig
from dunetuf.ui.new.shared.config_generator import ConfigGenerator, ConfigLoader
from dunetuf.ui.new.shared.navigation_handler import NavigationHandler
from dunetuf.ui.new.shared.global_state_manager import get_global_state_manager
from dunetuf.ui.new.shared.enums import Feature

# Original imports
from dunetuf.ui.new.shared.protocols.copy_ops import CopyOps
from dunetuf.ui.new.shared.decorators.measure_performance import measure_performance
from dunetuf.ui.new.dune.workflow.locators.copy import CopyLoc
from dunetuf.ui.new.shared.driver import ClickConfig
from dunetuf.ui.new.ui import UI


class WorkflowCopyOpsCommon(CopyOps):
    """
    Common Copy Operations implementation using configuration-driven architecture.
    All states, transitions, and options are loaded from JSON/YAML configuration.
    """
    
    def __init__(
        self,
        ui: "UI",
        size: str,
        type: str,
        validate_navigation: bool = True
    ):
        """
        Initialize with hierarchical configuration files.
        
        Args:
            ui: UI instance
            size: UI size (xl, l, m, s, xs)
            type: Type of workflow (e.g., "workflow")
            validate_navigation: Whether to validate state transitions
        """
        self.ui = ui
        self.size = size
        self.type = type
        self._driver = ui._driver
        self.validate_navigation = validate_navigation
        
        # Setup logging
        self._logger = self._setup_logging()
        
        # Configuration directory
        config_dir = Path(__file__).parent.parent / "config"
        
        self._logger.info(f"Loading hierarchical configuration from {config_dir}")
        
        # Initialize configuration generator with hierarchical config
        self._config_generator = ConfigGenerator.from_size_config(
            size=size,
            type=type,
            feature="copy",
            config_dir=config_dir,
            locator_module=CopyLoc,
            logger=self._logger
        )
        
        # Get generated components
        self._state_machine = self._config_generator.get_state_machine()
        self._option_configs = self._config_generator.get_options()
        self._metadata = self._config_generator.get_metadata()
        
        # Initialize option handler
        self._option_handler = GenericOptionHandler(self._driver, self._logger, self._config_generator)
        
        # Performance metrics
        self._performance_metrics: Dict[str, List[float]] = {}
                
        # Initialize state detection
        self._initialize_state_detection()

        self._navigation_handler = NavigationHandler(
            driver=self._driver,
            locator_provider=CopyLoc,
            logger=self._logger,
            state_machine=self._state_machine,
            config_generator=self._config_generator,
            option_handler=self._option_handler,
            option_configs=self._option_configs,            
            metadata=self._metadata,
            performance_metrics=self._performance_metrics,
            feature=Feature.COPY
        )

        self._global_state_manager = get_global_state_manager()

        # Setup state machine listeners
        self._setup_state_listeners()
        
        self._logger.info(f"Initialized {self._metadata['name']} v{self._metadata['version']}")
    
    def _setup_logging(self) -> logging.Logger:
        """Setup logging configuration."""
        logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.DEBUG)
        
        return logger
    
    def _setup_state_listeners(self) -> None:
        """Setup state machine event listeners."""
        
        def on_state_change(from_state: str, to_state: str) -> None:
            """Log state transitions."""
            self._logger.info(f"State transition: {from_state} -> {to_state}")
            
            # Record performance metric
            if hasattr(self, '_transition_start_time'):
                elapsed = time.time() - self._navigation_handler._transition_start_time
                self._navigation_handler._record_metric(f"transition_{from_state}_to_{to_state}", elapsed)
        
        self._state_machine.add_listener(on_state_change)
    
    def _initialize_state_detection(self) -> None:
        """Initialize current state detection."""
        # Map states to their UI indicators
        state_indicators = {}
        
        for state_name, state in self._state_machine._states.items():
            if state.metadata.get("view_elements"):
                # Convert string references to actual locators
                elements = []
                for element_ref in state.metadata["view_elements"]:
                    try:
                        elements.append(getattr(CopyLoc, element_ref))
                    except AttributeError:
                        self._logger.warning(f"Unknown locator: {element_ref}")
                
                if elements:
                    state_indicators[state_name] = elements
        
        # Detect current state
        current_state = self._detect_current_state(state_indicators)
        if current_state:
            self._state_machine._current_state = current_state
            self._logger.info(f"Initial state detected: {current_state}")
    
    def _detect_current_state(self, state_indicators: Dict[str, List]) -> Optional[str]:
        """Detect current UI state based on visible elements."""
        for state_name, indicators in state_indicators.items():
            try:
                if all(self._driver.exists(indicator) for indicator in indicators):
                    return state_name
            except Exception as e:
                self._logger.debug(f"Error checking state {state_name}: {e}")
        
        return None
    
    # ========== Convenience Navigation Methods ==========
    
    def goto_copy_landing_page(self) -> None:
        """Navigate to copy landing page."""
        self._navigation_handler.navigate_to("COPY_LANDING")
    
    def goto_copy_widget_page(self) -> None:
        """Navigate to copy widget page."""
        self._navigation_handler.navigate_to("COPY_WIDGET_CARD")
    
    def goto_copy_options_list(self) -> None:
        """Navigate to copy options list."""
        self._navigation_handler.navigate_to("COPY_OPTIONS_LIST")

    def goto_copy_resolution_list(self) -> None:
        """Navigate to copy resolution list."""
        self._navigation_handler.navigate_to("COPY_RESOLUTION_LIST")

    def goto_copy_content_type_list(self) -> None:
        """Navigate to copy content type list."""
        self._navigation_handler.navigate_to("COPY_CONTENT_TYPE_LIST")

    def goto_copy_original_paper_list(self) -> None:
        """Navigate to copy original paper type list."""
        self._navigation_handler.navigate_to("COPY_ORIGINAL_PAPER_LIST")
    
    def go_back_to_copy_landing(self) -> None:
        """Navigate back to copy landing."""
        self._navigation_handler.navigate_to("COPY_LANDING")

    
    
   
    # ========== Specific Option Methods (for compatibility) ==========
    
    def select_color_mode(self, option: str) -> None:
        """Select color mode option."""
        self._navigation_handler.select_option("color_mode", option)
    
    def select_original_paper_type(self, option: str) -> None:
        """Select original paper type."""
        self._navigation_handler.select_option("original_paper_type", option)
    
    def select_content_type(self, option: str) -> None:
        """Select content type."""
        self._navigation_handler.select_option("content_type", option)
    
    def select_resolution(self, option: str) -> None:
        """Select resolution."""
        self._navigation_handler.select_option("resolution", option)
    
    def toggle_invert_blueprints(self, enable: bool) -> None:
        """Toggle invert blueprints option."""
        self._navigation_handler.select_option("invert_blueprints", enable)
    
    def select_number_of_copies(self, count: int) -> None:
        """Set number of copies."""
        self._navigation_handler.select_option("number_of_copies", count)
    
    # ========== Action Methods ==========
    
    @measure_performance("Click Start Button")
    def click_start(self) -> None:
        """Click the Start button to initiate copying."""
        # Ensure we're on copy landing page
        if self._state_machine.current_state != "COPY_LANDING":
            self._navigation_handler.navigate_to("COPY_LANDING")
        
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
            
            time.sleep(1)  # Wait for action to register
            
            self._logger.info("Successfully clicked Start button")
            self._navigation_handler._record_metric("start_button_click", 1)
            
        except Exception as e:
            self._logger.error(f"Failed to click Start button: {e}")
            self._navigation_handler._take_screenshot_on_error("click_start")
            raise
    
    # ========== Batch Operations ==========

    def apply_preset(self, preset_name: str) -> None:
        """
        Apply a preset configuration of options.
        
        Args:
            preset_name: Name of preset to apply
        """
        presets = {
            "high_quality_color": {
                "color_mode": "Color",
                "resolution": "600dpi",
                "content_type": "Mixed"
            },
            "fast_bw": {
                "color_mode": "Black Only",
                "resolution": "200dpi",
                "content_type": "Text"
            },
            "photo_copy": {
                "color_mode": "Color",
                "resolution": "600dpi",
                "content_type": "Photograph",
                "original_paper_type": "photo"
            },
            "blueprint": {
                "original_paper_type": "blueprint",
                "invert_blueprints": True,
                "color_mode": "Grayscale"
            }
        }

        if preset_name not in presets:
            raise ValueError(f"Unknown preset: {preset_name}")

        preset = presets[preset_name]
        self._logger.info(f"Applying preset: {preset_name}")

        for option_name, value in preset.items():
            try:
                self._navigation_handler.select_option(option_name, value)
            except Exception as e:
                self._logger.error(f"Failed to set {option_name}: {e}")
    
    def batch_configure(self, options: Dict[str, Any]) -> Dict[str, bool]:
        """
        Configure multiple options at once.
        
        Args:
            options: Dictionary of option_name: value pairs
            
        Returns:
            Dictionary of option_name: success status
        """
        results = {}
        
        for option_name, value in options.items():
            try:
                self._navigation_handler.select_option(option_name, value)
                results[option_name] = True
            except Exception as e:
                self._logger.error(f"Failed to set {option_name}: {e}")
                results[option_name] = False
        
        return results
    
    # ========== Utility Methods ==========
    
    def get_performance_report(self) -> str:
        """Generate performance report."""
        report = ["Performance Report", "=" * 50]
        
        for metric_name, values in sorted(self._performance_metrics.items()):
            if values:
                avg_value = sum(values) / len(values)
                max_value = max(values)
                min_value = min(values)
                
                report.append(f"\n{metric_name}:")
                report.append(f"  Count: {len(values)}")
                report.append(f"  Average: {avg_value:.3f}")
                report.append(f"  Min: {min_value:.3f}")
                report.append(f"  Max: {max_value:.3f}")
        
        return "\n".join(report)
    
    def export_documentation(self, output_path: Optional[Path] = None) -> str:
        """
        Export auto-generated documentation.
        
        Args:
            output_path: Optional path to save documentation
            
        Returns:
            Documentation as string
        """
        return self._config_generator.export_documentation(output_path)
    
    def get_current_configuration(self) -> Dict[str, Any]:
        """Get current values of all options."""
        config = {}
        
        for option_name, option_config in self._option_configs.items():
            try:
                value = self._option_handler.get_current_value(option_config)
                config[option_name] = value
            except Exception as e:
                self._logger.debug(f"Could not get value for {option_name}: {e}")
                config[option_name] = None
        
        return config
    
    def reset_to_defaults(self) -> None:
        """Reset all options to their default values."""
        self._logger.info("Resetting all options to defaults")
        
        for option_name, option_config in self._option_configs.items():
            if option_config.default_value is not None:
                try:
                    self._navigation_handler.select_option(option_name, option_config.default_value)
                except Exception as e:
                    self._logger.error(f"Failed to reset {option_name}: {e}")

    def force_goto_state(self, target_state: str) -> None:
        """
        Force navigation to target state without UI actions.
        Useful for state synchronization and testing.
        
        Args:
            target_state: Target state to force transition to
        """
        self._logger.info(f"FORCE GOTO: {target_state} (no UI interaction)")
        self._navigation_handler.force_state_transition(target_state)
    
    def sync_with_current_ui_state(self) -> str:
        """
        Detect current UI state and synchronize state machine.
        
        Returns:
            str: The detected current state
        """
        # Use existing state detection logic
        state_indicators = self._build_state_indicators()
        detected_state = self._detect_current_state(state_indicators)
        
        if detected_state:
            self._navigation_handler.sync_state_with_ui(detected_state)
            return detected_state
        else:
            self._logger.warning("Could not detect current UI state")
            return "UNKNOWN"
    
    def _build_state_indicators(self) -> Dict[str, List]:
        """Build state indicators mapping from state machine metadata."""
        state_indicators = {}
        
        for state_name, state in self._state_machine._states.items():
            if state.metadata.get("view_elements"):
                elements = []
                for element_ref in state.metadata["view_elements"]:
                    try:
                        elements.append(getattr(CopyLoc, element_ref))
                    except AttributeError:
                        self._logger.warning(f"Unknown locator: {element_ref}")
                
                if elements:
                    state_indicators[state_name] = elements
        
        return state_indicators


    def go_home(self) -> bool:
        """Go to HOME screen using global navigation."""
        try:
            self._logger.info("Navigating to HOME via global state manager")
            
            # Use global navigation
            success = self._navigation_handler.navigate_to_global_home()
            
            if success:
                self._logger.info("Successfully navigated to HOME")
                # Update performance metrics
                #self._record_operation_metric("navigate_to_home", 1.0)
            else:
                self._logger.error("Failed to navigate to HOME")
            
            return success
            
        except Exception as e:
            self._logger.error(f"Home navigation failed: {e}")
            self._navigation_handler.take_screenshot_on_error("go_home_failed")
            return False
    
    def get_current_location(self) -> Dict[str, Any]:
        """Get current location information."""
        return {
            "local_state": self._state_machine.current_state,
            "global_status": self._global_state_manager.export_status_report(),
            "can_exit_to_home": self._global_state_manager.can_exit_to_home(),
            "navigation_path_to_home": self._global_state_manager.get_navigation_path_to_home()
        }