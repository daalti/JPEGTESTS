# shared/protocols/copy_logic.py
from typing import Protocol
from .copy_ops import CopyOps

class CopyLogic(Protocol):
    def execute(self, ops: CopyOps, state, ui) -> str: ...
