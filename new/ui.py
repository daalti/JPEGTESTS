# dunetuf/ui/new/shared/base.py
from __future__ import annotations
import importlib
from functools import cached_property
from typing import Any, Type, TypeVar, cast
from typing_extensions import Self # type: ignore
from dunetuf.control.targetdevice import TargetPlatform, device_instance
from dunetuf.udw.udw import get_underware_instance
from dunetuf.metadata import get_ip
from dunetuf.ui.new.shared.enums import Platform, UIType, UISize, Feature, norm_platform, norm_uitype, norm_uisize
from dunetuf.ui.new.shared.decorators.feature_registry import FeatureRegistry
from dunetuf.ui.new.fluent.copy import CopyDSL
from dunetuf.ui.new.shared.driver import QmlDriver, QmlDriverConfig

T = TypeVar("T", bound="UI")

def _feature_modpath(platform: Platform, uitype: UIType, uisize: UISize, feature: Feature) -> str:
    # e.g.: dunetuf.ui.new.dune.workflow.xl.copy_ops
    return f"dunetuf.ui.new.{platform.value}.{uitype.value}.{uisize.value}.{feature.value}_ops"

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

    # Resolve feature provider (registry + lazy import)
    def _resolve_feature_provider(self, feature: Feature):
        provider_cls = FeatureRegistry.resolve(self._platform, self._uiType, self._uiSize, feature)
        if not provider_cls:
            try:
                importlib.import_module(_feature_modpath(self._platform, self._uiType, self._uiSize, feature))
            except ModuleNotFoundError:
                pass
            provider_cls = FeatureRegistry.resolve(self._platform, self._uiType, self._uiSize, feature)
        if not provider_cls:
            raise NotImplementedError(f"No provider for ({self._platform.value}, {self._uiType.value}, {self._uiSize.value}, {feature.value})")
        return provider_cls(self)  # instantiate with the UI (or with udw if preferred)

    # Facade → DSLs
    @cached_property
    def copy(self) -> "CopyDSL":
        from dunetuf.ui.new.fluent.copy import CopyDSL
        return CopyDSL(self)
