# dunetuf/ui/new/shared/enums.py
from enum import Enum
from typing import Union

class Platform(str, Enum):
    DUNE = "dune"
    ARES = "ares"

class UIType(str, Enum):
    PROSELECT = "proselect"
    WORKFLOW = "workflow"
    WORKFLOW2 = "workflow2"

class UISize(str, Enum):
    XS = "xs"; S = "s"; M = "m"; L = "l"; XL = "xl"

class Feature(str, Enum):
    COPY = "copy"
    PRINT = "print"

class Logic(str, Enum):
    COPY = "copy"
    PRINT = "print"

def _coerce(v) -> str:
    if isinstance(v, Enum):
        return str(v.value)
    return str(v)

def norm_platform(s: Union[str, Platform]) -> Platform:
    return Platform(_coerce(s).lower())

def norm_uitype(s: Union[str, UIType]) -> UIType:
    return UIType(_coerce(s).lower())

def norm_uisize(s: Union[str, UISize]) -> UISize:
    return UISize(_coerce(s).lower())
