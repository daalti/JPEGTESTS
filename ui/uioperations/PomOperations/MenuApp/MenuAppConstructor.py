import logging

from .Menu import Menu
from .MenuApp import MenuApp
from .MenuAppS import MenuAppS

class MenuAppConstructor():
    @staticmethod
    def construct(spice) -> Menu:
        logging.info(f"TYPE: {spice.uitype}, SIZE: {spice.uisize}")
        if spice.uitype == "Workflow":
            if spice.uisize == "S":
                return MenuAppS(spice)
            if spice.uisize == "L":
                return MenuApp(spice)
            if spice.uisize == "XL":
                return MenuApp(spice)
        elif spice.uitype == "Workflow2":
            #{PR114945} TODO Add the code here
            logging.debug("Not Implemented")
            pass
        elif spice.uitype == "ProSelect":
            logging.debug("Not Implemented")
            return None
        else:
            logging.debug("Not Implemented")
            return None