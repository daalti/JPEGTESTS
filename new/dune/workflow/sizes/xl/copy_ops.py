"""
XL Copy Operations - Inherits from Common Base
Size-specific implementation for XL screens
"""

from dunetuf.ui.new.dune.workflow.common.copy_ops import WorkflowCopyOpsCommon
from dunetuf.ui.new.ui import UI


class WorkflowXLCopyOps(WorkflowCopyOpsCommon):
    """
    XL Copy Operations implementation.
    Inherits all functionality from WorkflowCopyOpsCommon.
    Can be extended with XL-specific functionality as needed.
    """
    
    def __init__(
        self,
        ui: "UI",
        validate_navigation: bool = True
    ):
        """
        Initialize XL Copy Operations.
        
        Args:
            ui: UI instance
            validate_navigation: Whether to validate state transitions
        """
        # Initialize with size "xl"
        super().__init__(ui, size="xl", type="workflow", validate_navigation=validate_navigation)


# ========== Usage Example ==========

def example_usage():
    """Example of how to use the XL copy operations."""
    
    # Initialize UI (mock for example)
    ui = UI()  # Your UI instance
    
    # Create copy operations with configuration
    copy_ops = WorkflowXLCopyOps(
        ui=ui
    )
    
    # Simple navigation
    copy_ops.goto_copy_landing_page()
    
    # Configure options
    copy_ops.select_color_mode("Color")
    copy_ops.select_resolution("600dpi")
    copy_ops.select_number_of_copies(5)
    
    # Or use batch configuration
    copy_ops.batch_configure({
        "color_mode": "Color",
        "resolution": "600dpi",
        "content_type": "Photograph",
        "number_of_copies": 3
    })
    
    # Or apply a preset
    copy_ops.apply_preset("high_quality_color")
    
    # Start copying
    copy_ops.click_start()
    
    # Get performance report
    print(copy_ops.get_performance_report())


if __name__ == "__main__":
    # Run example
    example_usage()