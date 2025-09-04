from dataclasses import dataclass
from dunetuf.ui.new.shared.enums import Feature
from dunetuf.ui.new.shared.decorators.copy_logic_registry import CopyLogicRegistry
from dunetuf.ui.new.ui import UI

@dataclass
class _CopyState:
    tray: str = "tray-1"
    color: str = "mono"
    duplex: str = "off"

class CopyDSL:
    def __init__(self, ui: "UI") -> None:
        self._ui = ui
        self._s = _CopyState()
        self._ops = ui._resolve_feature_provider(Feature.COPY)

    def source(self, tray: str) -> "CopyDSL": self._s.tray = tray; return self
    def color(self, c: str) -> "CopyDSL": self._s.color = c; return self
    def duplex(self, d: str) -> "CopyDSL": self._s.duplex = d; return self

    def start_copy(self, *, tray: str|None=None, color: str|None=None, duplex: str|None=None) -> str:
        if tray: self._s.tray = tray
        if color: self._s.color = color
        if duplex: self._s.duplex = duplex
        self._ops.open_app()
        self._ops.select_source_tray(self._s.tray)
        self._ops.set_color(self._s.color)
        self._ops.set_duplex(self._s.duplex)
        return self._ops.press_start()
