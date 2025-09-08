# shared/protocols/copy_ops.py
from typing import Protocol, List
from dataclasses import dataclass


class CopyOps(Protocol):
    
    
    def goto_copy_landing_page(self) -> None:
        '''
        UI should be inside cpy app from home screen'
        Navigation Home >> copy option >> copylanding view
        '''
        raise NotImplementedError("goto_copy_landing_page not implemented. Should be implemented by subclass.")
    
    def goto_copy_widget_page(self) -> None:
        '''
        UI should be inside cpy app from home screen'
        Navigation Home >> copy option >> widget copy view
        '''
        raise NotImplementedError("goto_copy_widget_page not implemented. Should be implemented by subclass.")
    
    def goto_copy_options_list(self) -> None:
        '''
        Navigate to copy options list from copy landing page
        '''
        raise NotImplementedError("goto_copy_options_list not implemented. Should be implemented by subclass.")

    def select_color_mode(self, option: str) -> None:
        '''
        Select color mode from copy landing page
        color_mode: str : "Automatic", "Color", "Grayscale", "Black Only"
        '''
        raise NotImplementedError("select_color_mode not implemented. Should be implemented by subclass.")
    
    def select_original_paper_type(self, option: str) -> None:
        '''
        Select original paper type from copy landing page
        paper_type: str : "Plain", "Thick", "Thin", "Transparency", "Label", "Envelope"
        '''
        raise NotImplementedError("select_original_paper_type not implemented. Should be implemented by subclass.")
    
    def select_content_type(self, option: str) -> None:
        '''
        Select content type from copy landing page
        option: str : 
                - "Mixed": Mixed content
                 - "Photograph": Photograph content
                 - "Text": Text content
                 - "Lines": Line art content
                 - "Image": Image content
        '''
        raise NotImplementedError("select_content_type not implemented. Should be implemented by subclass.")
    
    def select_resolution(self, option: str) -> None:
        '''
        Select resolution from copy landing page
        option: str : 
                 - "200dpi": 200 DPI
                 - "300dpi": 300 DPI
                 - "600dpi": 600 DPI
        '''
        raise NotImplementedError("select_resolution not implemented. Should be implemented by subclass.")
    
    def toggle_invert_blueprints(self, enable: bool) -> None:
        '''
        Enable or disable the invert blueprints setting for copying.
        Args:
            enable (bool): True to enable invert blueprints, False to disable.
        '''
        raise NotImplementedError("toggle_invert_blueprints not implemented. Should be implemented by subclass.")
    
    def select_number_of_copies(self, count: int) -> None:
        '''
        Select number of copies from copy landing page
        count: int : Number of copies to be made (e.g., 1, 2, 3, ...)
        '''
        raise NotImplementedError("select_number_of_copies not implemented. Should be implemented by subclass.")
    
    def click_start(self) -> None:
        '''
        Click on start button from copy landing page
        '''
        raise NotImplementedError("click_start_button not implemented. Should be implemented by subclass.")
    
    def go_back_to_copy_landing(self) -> None:
        '''
        Go back to copy landing page from copy options list page
        '''
        raise NotImplementedError("go_back_to_copy_landing not implemented. Should be implemented by subclass.")
