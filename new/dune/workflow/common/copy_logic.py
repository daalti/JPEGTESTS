"""
Common Copy Logic with Configuration-Based Architecture
Base implementation for all sizes
"""

import time
from dunetuf.ui.new.shared.decorators.copy_logic_registry import CopyLogicRegistry
from dunetuf.ui.new.shared.enums import Platform, UIType, UISize, Logic
from dunetuf.ui.new.shared.protocols.copy_logic import CopyLogic
from dunetuf.ui.new.shared.protocols.copy_ops import CopyOps
from dunetuf.ui.new.ui import UI


class WorkflowCopyLogicCommon(CopyLogic):
    """
    Common Copy Logic implementation using configuration-driven architecture.
    Base class that can be extended by size-specific implementations.
    """

    def __init__(self, ui: UI, copy_ops: CopyOps) -> None:
        """
        Initialize with UI and copy operations.
        
        Args:
            ui: UI instance
            copy_ops: Copy operations instance
        """
        self._ui = ui
        self._copy_ops = copy_ops

    def from_copy_landing_page(self) -> None:
        """
        Navigate to the Copy Landing Page.
        """
        self._copy_ops.goto_copy_landing_page()

    def from_copy_option_list(self) -> None:
        """
        Navigate to the Copy Options List Page.
        """
        self._copy_ops.goto_copy_options_list()


    def from_widget_copy_page(self) -> None:
        """
        Navigate to the Widget Copy Page.
        """
        self._copy_ops.goto_copy_widget_page()

    def set_color_mode(self, mode: str) -> None:
        """
        Set the color mode for copying.
        Args:
            mode (str): The color mode to set. Options are "Automatic", "Color", "Grayscale", "Black Only".
        
        Raises:
            ValueError: If an invalid mode is provided.
        """
        self._copy_ops.select_color_mode(mode)

    def set_original_paper_type(self, paper_type: str) -> None:
        """
        Set the original paper type for copying.
        Args:
            paper_type (str): The paper type to set. Options are "Plain", "Thick", "Thin", "Transparency", "Label", "Envelope", "Cardstock".
        
        Raises:
            ValueError: If an invalid paper type is provided.
        """
        self._copy_ops.select_original_paper_type(paper_type)

    def set_content_type(self, option: str) -> None:
        """
        Set the content type for copying.
        Args:
            option (str): The content type option to set. Options are:
                - "Mixed": Mixed content
                - "Photograph": Photograph content
                - "Text": Text content
                - "Lines": Line art content
                - "Image": Image content
        
        Raises:
            ValueError: If an invalid content type option is provided.
            RuntimeError: If content type selection fails.
        """
        self._copy_ops.goto_copy_content_type_list()
        self._copy_ops.select_content_type(option)

    def set_resolution(self, option: str) -> None:
        """
        Set the resolution for copying.
        Args:
            option (str): The resolution option to set. Options are:
                - "200dpi": 200 DPI
                - "300dpi": 300 DPI
                - "600dpi": 600 DPI
        
        Raises:
            ValueError: If an invalid resolution option is provided.
            RuntimeError: If resolution selection fails.
        """
        #self._copy_ops.goto_copy_resolution_list()
        self._copy_ops.select_resolution(option)

    def set_invert_blueprints(self, enable: bool) -> None:
        """
        Enable or disable the invert blueprints setting for copying.
        Args:
            enable (bool): True to enable invert blueprints, False to disable.
        """
        self._copy_ops.toggle_invert_blueprints(enable)

    def set_number_of_copies(self, count: int) -> None:
        """
        Set the number of copies to be made.
        Args:
            count (int): The number of copies to set. Must be a positive integer.
        
        Raises:
            ValueError: If count is not a positive integer.
        """
        self._copy_ops.select_number_of_copies(count)

    def start(self) -> None:
        """
        Start the copy operation.
        """
        self._copy_ops.click_start()

    def go_back_to_copy_landing(self) -> None:
        """
        Navigate back to the Copy Landing Page from the current settings view.
        """
        self._copy_ops.go_back_to_copy_landing()