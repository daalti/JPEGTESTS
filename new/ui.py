# dunetuf/ui/new/shared/base.py
from __future__ import annotations
import importlib
from functools import cached_property
from typing import Any, Type, TypeVar, cast
from typing_extensions import Self # type: ignore
from dunetuf.control.targetdevice import TargetPlatform, device_instance
from dunetuf.udw.udw import get_underware_instance
from dunetuf.metadata import get_ip
from dunetuf.ui.new.shared.enums import Platform, UIType, UISize, Logic, norm_platform, norm_uitype, norm_uisize
from dunetuf.ui.new.shared.driver import QmlDriver
from dunetuf.ui.new.shared.protocols.copy_logic import CopyLogic
from dunetuf.ui.new.shared.decorators.copy_logic_registry import CopyLogicRegistry

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
