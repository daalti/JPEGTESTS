"""
XL Copy Logic - Inherits from Common Base
Size-specific implementation for XL screens
"""

from dunetuf.ui.new.dune.workflow.common.copy_logic import WorkflowCopyLogicCommon
from dunetuf.ui.new.dune.workflow.sizes.xl.copy_ops import WorkflowXLCopyOps
from dunetuf.ui.new.shared.decorators.copy_logic_registry import CopyLogicRegistry
from dunetuf.ui.new.shared.enums import Platform, UIType, UISize, Logic
from dunetuf.ui.new.ui import UI


@CopyLogicRegistry.register(Platform.DUNE, UIType.WORKFLOW, UISize.XL, Logic.COPY)
class WorkflowXLCopyLogic(WorkflowCopyLogicCommon):
    """
    XL Copy Logic implementation.
    Inherits all functionality from WorkflowCopyLogicCommon.
    Can be extended with XL-specific functionality as needed.
    """

    def __init__(self, ui: UI) -> None:
        """
        Initialize XL Copy Logic.
        
        Args:
            ui: UI instance
        """
        # Create XL-specific copy operations
        copy_ops = WorkflowXLCopyOps(ui)
        
        # Initialize base class with copy operations
        super().__init__(ui, copy_ops)