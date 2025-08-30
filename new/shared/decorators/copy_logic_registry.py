# shared/copy_logic_registry.py
from typing import Dict, Tuple, Type, Optional
from dunetuf.ui.new.shared.enums import Platform, UIType, UISize
from dunetuf.ui.new.shared.protocols.copy_logic import CopyLogic

Key = Tuple[Platform, UIType, UISize]

class CopyLogicRegistry:
    _map: Dict[Key, Type[CopyLogic]] = {}
    @classmethod
    def register(cls, p, t, s):
        def _wrap(kls: Type[CopyLogic]):
            cls._map[(p, t, s)] = kls; return kls
        return _wrap
    @classmethod
    def resolve(cls, p, t, s) -> Optional[Type[CopyLogic]]:
        return cls._map.get((p, t, s))
