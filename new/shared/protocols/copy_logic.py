# shared/protocols/copy_logic.py
from typing import Protocol, Dict, Any
from .copy_ops import CopyOps
from typing_extensions import Self #type: ignore

class CopyLogic(Protocol):

    def goto_copy_landing_page(self) -> None:
        """
        Navigate to the Copy Landing Page.
        """
        raise NotImplementedError("goto_copy_landing_page method not implemented")

    def goto_widget_copy_page(self) -> None:
        """
        Navigate to the Widget Copy Page.
        """
        raise NotImplementedError("goto_widget_copy_page method not implemented")
    
    def goto_copy_option_list(self) -> None:
        """
        Navigate to the Copy Options List Page.
        """
        raise NotImplementedError("goto_copy_option_list method not implemented")

    def from_copy_landing_page(self) -> Self:
        """
        Navigate to the Copy Landing Page.
        
        Returns:
            Self: This instance for method chaining
        """
        raise NotImplementedError("from_copy_landing_page method not implemented")
    
    def from_widget_copy_page(self) -> Self:
        """
        Navigate to the Widget Copy Page.
        
        Returns:
            Self: This instance for method chaining
        """
        raise NotImplementedError("from_widget_copy_page method not implemented")

    def from_copy_option_list(self) -> Self:
        """
        Navigate to the Copy Options List Page.
        
        Returns:
            Self: This instance for method chaining
        """
        raise NotImplementedError("from_copy_option_list method not implemented")

    def set_color_mode(self, mode: str) -> None:
        """
        Set the color mode for copying.
        Args:
            mode (str): The color mode to set. Options are "Automatic", "Color", "Grayscale", "Black Only".
        
        Raises:
            ValueError: If an invalid mode is provided.
        """
        raise NotImplementedError("set_color_mode method not implemented")
    
    def set_original_paper_type(self, paper_type: str) -> None:
        """
        Set the original paper type for copying.
        Args:
            paper_type (str): The paper type to set. Options are "Plain", "Thick", "Thin", "Transparency", "Label", "Envelope".
        
        Raises:
            ValueError: If an invalid paper type is provided.
        """
        raise NotImplementedError("set_original_paper_type method not implemented")
    
    def set_content_type(self, option: str) -> None:
        """
        Set the content type for copying.
        Args:
            option (str): The content type option to set. Options are "Mixed", "Photograph", "Text", "Lines", "Image".
        
        Raises:
            ValueError: If an invalid content type option is provided.
        """
        raise NotImplementedError("set_content_type method not implemented")

    def set_resolution(self, option: str) -> None:
        """
        Set the resolution for copying.
        Args:
            option (str): The resolution option to set. Options are "200dpi", "300dpi", "600dpi".
        
        Raises:
            ValueError: If an invalid resolution option is provided.
        """
        raise NotImplementedError("set_resolution method not implemented")
    
    def set_invert_blueprints(self, enable: bool) -> None:
        """
        Enable or disable the invert blueprints setting for copying.
        Args:
            enable (bool): True to enable invert blueprints, False to disable.
        """
        raise NotImplementedError("set_invert_blueprints method not implemented")

    def set_number_of_copies(self, count: int) -> None:
        """
        Set the number of copies to make.
        Args:
            count (int): The number of copies to set. Must be a positive integer.
        
        Raises:
            ValueError: If count is not a positive integer.
        """
        raise NotImplementedError("set_number_of_copies method not implemented")

    def with_color_mode(self, mode: str) -> Self:
        """
        Set the color mode for copying and return self for method chaining.
        Args:
            mode (str): The color mode to set. Options are "Automatic", "Color", "Grayscale", "Black Only".
        
        Returns:
            Self: This instance for method chaining
        """
        raise NotImplementedError("with_color_mode method not implemented")

    def with_original_paper_type(self, paper_type: str) -> Self:
        """
        Set the original paper type for copying and return self for method chaining.
        Args:
            paper_type (str): The paper type to set. Options are "Plain", "Thick", "Thin", "Transparency", "Label", "Envelope".
        
        Returns:
            Self: This instance for method chaining
        """
        raise NotImplementedError("with_original_paper_type method not implemented")
    
    def with_content_type(self, option: str) -> Self:
        """
        Set the content type for copying and return self for method chaining.
        Args:
            option (str): The content type option to set. Options are "Mixed", "Photograph", "Text", "Lines", "Image".
        
        Returns:
            Self: This instance for method chaining
        """
        raise NotImplementedError("with_content_type method not implemented")
    
    def with_resolution(self, option: str) -> Self:
        """
        Set the resolution for copying and return self for method chaining.
        Args:
            option (str): The resolution option to set. Options are "200dpi", "300dpi", "600dpi".
        
        Returns:
            Self: This instance for method chaining
        """
        raise NotImplementedError("with_resolution method not implemented")
    
    def with_invert_blueprints(self, enable: bool) -> Self:
        """
        Enable or disable the invert blueprints setting for copying and return self for method chaining.
        Args:
            enable (bool): True to enable invert blueprints, False to disable.
        Returns:
            Self: This instance for method chaining
        """
        raise NotImplementedError("with_invert_blueprints method not implemented")
    
    def with_number_of_copies(self, count: int) -> Self:
        """
        Set the number of copies to make and return self for method chaining.
        Args:
            count (int): The number of copies to set. Must be a positive integer.
        Returns:
            Self: This instance for method chaining
        """
        raise NotImplementedError("with_number_of_copies method not implemented")

    def batch_configure(self, ops: Dict[str, Any]) -> None:
        """
        Perform a batch copy operation with the specified options.
        Args:
            ops Dict[str, Any]: The copy operations to perform.
        """
        raise NotImplementedError("batch_configure method not implemented")

    def start(self, mdf_loaded: bool = False) -> None:
        """
        Start the copy operation.
        Args:
            mdf_loaded (bool): True if MDF is loaded, False otherwise.
        """
        raise NotImplementedError("start method not implemented")
    
    def go_back_to_copy_landing(self) -> None:
        """
        Navigate back to the Copy Landing Page.
        """
        raise NotImplementedError("go_back_to_copy_landing method not implemented")
