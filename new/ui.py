# dunetuf/ui/new/shared/base.py
from __future__ import annotations
import importlib
import logging
from functools import cached_property
from typing import Any, Type, TypeVar, cast
from typing_extensions import Self # type: ignore
from dunetuf.control.targetdevice import TargetPlatform, device_instance
from dunetuf.udw.udw import get_underware_instance
from dunetuf.metadata import get_ip
from dunetuf.ui.new.shared.enums import Platform, UIType, UISize, Logic, Feature, norm_platform, norm_uitype, norm_uisize
from dunetuf.ui.new.shared.driver import QmlDriver
from dunetuf.ui.new.shared.protocols.copy_logic import CopyLogic
from dunetuf.ui.new.shared.decorators.copy_logic_registry import CopyLogicRegistry
from dunetuf.ui.new.shared.global_state_manager import get_global_state_manager

T = TypeVar("T", bound="UI")

def _logic_modpath(platform: Platform, uitype: UIType, uisize: UISize, logic: Logic) -> str:
    # e.g.: dunetuf.ui.new.dune.workflow.xl.copy_logic
    return f"dunetuf.ui.new.{platform.value}.{uitype.value}.sizes.{uisize.value}.{logic.value}_logic"

class UI:
    def __new__(cls: Type[Self], *args: Any, **kwargs: Any) -> Self:
        if cls is UI:
            # Discover current context
            plat = device_instance().target_platform
            cls._platform = norm_platform(Platform.DUNE if plat == TargetPlatform.DUNE else Platform.ARES)

            # Read uitype/uisize
            cls._ip_address = get_ip()
            cls._udw = get_underware_instance(ip = cls._ip_address)
            cls._uiType = norm_uitype(cls._udw.mainUiApp.ControlPanel.getExperience()) #type: ignore
            cls._uiSize = norm_uisize(cls._udw.mainUiApp.ControlPanel.getBreakPoint()) #type: ignore

            return cast(Self, super().__new__(cls))
        return cast(Self, super().__new__(cls))

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self._driver = QmlDriver()
        self._logger = logging.getLogger(__name__)
        self._global_state_manager = get_global_state_manager()
    
    def _resolve_copy_logic(self, logic: Logic):
        logic_cls = CopyLogicRegistry.resolve(self._platform, self._uiType, self._uiSize, logic)
        if not logic_cls:
            try:
                importlib.import_module(_logic_modpath(self._platform, self._uiType, self._uiSize, logic))
            except ModuleNotFoundError:
                pass
            logic_cls = CopyLogicRegistry.resolve(self._platform, self._uiType, self._uiSize, logic)
        if not logic_cls:
            raise NotImplementedError(
                f"No CopyLogic for ({self._platform.value}, {self._uiType.value}, {self._uiSize.value}, {logic.value})"
            )
        return logic_cls(self) #type: ignore

    @cached_property
    def copy(self) -> CopyLogic:
        return self._resolve_copy_logic(Logic.COPY)
    
    def goto_homescreen(self) -> bool:
        """
        Navigate to home screen from any current location.
        Uses the GlobalStateManager to handle navigation across all features.
        
        Returns:
            bool: True if navigation successful, False otherwise
        """
        try:
            self._logger.info("UI.goto_homescreen: Attempting to navigate to home screen")
            
            # Get current status for logging
            current_status = self._global_state_manager.export_status_report()
            current_feature = current_status.get("current_feature")
            current_state = current_status.get("current_state")
            
            self._logger.info(f"Current location: {current_feature}:{current_state}")           
           
            # Perform navigation
            success = self._global_state_manager.navigate_to_home()
            
            if success:
                self._logger.info("Successfully navigated to home screen")
                
                # Update global state to HOME feature
                self._global_state_manager.set_current_feature(Feature.HOME)
            else:
                self._logger.error("Failed to navigate to home screen")
            
            return success
            
        except Exception as e:
            self._logger.error(f"Error during home screen navigation: {e}")
            return False
    
    def get_current_location(self) -> dict[str, Any]:
        """
        Get current UI location information.
        
        Returns:
            dict: Current location status including feature, state, and navigation capabilities
        """
        try:
            status = self._global_state_manager.export_status_report()
            
            # Add UI-specific information
            status.update({
                "platform": self._platform.value,
                "ui_type": self._uiType.value,
                "ui_size": self._uiSize.value,
                "ip_address": self._ip_address
            })
            
            return status
            
        except Exception as e:
            self._logger.error(f"Error getting current location: {e}")
            return {
                "error": str(e),
                "platform": self._platform.value,
                "ui_type": self._uiType.value,
                "ui_size": self._uiSize.value
            }
    
    def is_at_homescreen(self) -> bool:
        """
        Check if currently at home screen.
        
        Returns:
            bool: True if at home screen
        """
        try:
            return self._global_state_manager.is_at_home()
        except Exception as e:
            self._logger.error(f"Error checking home screen status: {e}")
            return False