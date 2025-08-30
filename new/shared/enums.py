# dunetuf/ui/new/shared/enums.py
from enum import Enum

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
    # SCAN = "scan"  # etc.

def norm_platform(s: str|Platform) -> Platform: return Platform(str(s).lower())
def norm_uitype(s: str|UIType) -> UIType: return UIType(str(s).lower())
def norm_uisize(s: str|UISize) -> UISize: return UISize(str(s).lower())
