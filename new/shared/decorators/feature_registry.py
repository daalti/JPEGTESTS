# dunetuf/ui/new/shared/feature_registry.py
from typing import Dict, Tuple, Type, Optional
from dunetuf.ui.new.shared.enums import Platform, UIType, UISize, Feature

Key = Tuple[Platform, UIType, UISize, Feature]

class FeatureRegistry:
    _map: Dict[Key, Type] = {}

    @classmethod
    def register(cls, platform: Platform, uitype: UIType, uisize: UISize, feature: Feature):
        def _wrap(kls: Type):
            cls._map[(platform, uitype, uisize, feature)] = kls
            return kls
        return _wrap

    @classmethod
    def resolve(cls, platform: Platform, uitype: UIType, uisize: UISize, feature: Feature) -> Optional[Type]:
        return cls._map.get((platform, uitype, uisize, feature))
