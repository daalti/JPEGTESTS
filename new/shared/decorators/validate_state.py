from typing import Callable
from dunetuf.ui.new.dune.workflow.xl.copy_ops import NavigationState, WorkflowXLCopyOps
from functools import wraps


def validate_state(expected_state: NavigationState):
    """Decorator to validate navigation state before operation."""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(self: 'WorkflowXLCopyOps', *args, **kwargs):
            if self.validate_navigation:
                current = self._get_current_state()
                if current != expected_state and expected_state != NavigationState.UNKNOWN:
                    self._logger.warning(
                        f"State mismatch: expected {expected_state.value}, got {current.value}"
                    )
            return func(self, *args, **kwargs)
        return wrapper
    return decorator