# shared/protocols/copy_ops.py
from typing import Protocol
from dataclasses import dataclass


class CopyOps(Protocol):
    
    def goto_copywidget_option_landingview(self) -> None:
        '''
        UI should be inside cpy app from home screen'
        Navigation Home >> copywidget option >> copylanding view
        '''
        raise NotImplementedError("goto_copywidget_option_landingview not implemented. Should be implemented by subclass.")
