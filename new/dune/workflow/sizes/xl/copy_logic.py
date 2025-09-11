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

    def start(self, mdf_loaded: bool = False) -> None:
        """
        Start the copy operation.
        Args:
            mdf_loaded: Indicates if MDF is loaded
        """
        if mdf_loaded:
            self._copy_ops.click_start()
        else:
            # Use common/base implementation - access parent's copy_ops
            # This calls WorkflowCopyOpsCommon.click_start() instead of WorkflowXLCopyOps.click_start()
            from dunetuf.ui.new.dune.workflow.common.copy_ops import WorkflowCopyOpsCommon
            
            # Create temporary common instance or call method directly
            # Option 1: Call super's method if available
            if hasattr(super(), '_copy_ops'):
                super()._copy_ops.click_start()
            else:
                # Option 2: Call the base class method directly on current instance
                WorkflowCopyOpsCommon.click_start(self._copy_ops)