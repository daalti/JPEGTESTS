# dunetuf/ui/new/shared/decorators/copy_logic_registry.py
from typing import Dict, Tuple, Type, Optional
from dunetuf.ui.new.shared.enums import Platform, UIType, UISize, Logic
from dunetuf.ui.new.shared.protocols.copy_logic import CopyLogic

Key = Tuple[Platform, UIType, UISize, Logic]

class CopyLogicRegistry:
    _map: Dict[Key, Type[CopyLogic]] = {}

    @classmethod
    def register(cls, platform: Platform, uitype: UIType, uisize: UISize, logic: Logic):
        def _wrap(kls: Type[CopyLogic]):
            cls._map[(platform, uitype, uisize, logic)] = kls
            return kls
        return _wrap

    @classmethod
    def resolve(
        cls,
        platform: Platform,
        uitype: UIType,
        uisize: UISize,
        logic: Logic
    ) -> Optional[Type[CopyLogic]]:
        return cls._map.get((platform, uitype, uisize, logic))
