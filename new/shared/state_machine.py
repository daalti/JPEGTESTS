"""
Generic State Machine Module
Reusable state machine implementation for UI navigation
"""

from typing import Dict, List, Optional, Callable, Any, Set, Tuple
from enum import Enum
from dataclasses import dataclass, field
from contextlib import contextmanager
import logging
import time
from abc import ABC, abstractmethod


class StateError(Exception):
    """Base exception for state machine errors."""
    pass


class TransitionError(StateError):
    """Exception raised when state transition fails."""
    pass


class State(ABC):
    """Abstract base class for states."""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Return state name."""
        pass
    
    @property
    def metadata(self) -> Dict[str, Any]:
        """Optional metadata for the state."""
        return {}
    
    def on_enter(self, context: Dict[str, Any]) -> None:
        """Called when entering this state."""
        pass
    
    def on_exit(self, context: Dict[str, Any]) -> None:
        """Called when exiting this state."""
        pass
    
    def can_transition_to(self, target_state: 'State', context: Dict[str, Any]) -> bool:
        """Check if transition to target state is allowed."""
        return True


@dataclass
class TransitionConfig:
    """Configuration for a state transition."""
    from_state: str
    to_state: str
    condition: Optional[Callable[[Dict[str, Any]], bool]] = None
    action: Optional[Callable[[Dict[str, Any]], None]] = None
    validators: List[Callable[[Dict[str, Any]], bool]] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def is_valid(self, context: Dict[str, Any]) -> bool:
        """Check if transition is valid in given context."""
        if self.condition and not self.condition(context):
            return False
        return all(validator(context) for validator in self.validators)
    
    def execute(self, context: Dict[str, Any]) -> None:
        """Execute transition action if defined."""
        if self.action:
            self.action(context)


class StateMachine:
    """Generic state machine implementation."""
    
    def __init__(self, initial_state: Optional[str] = None, logger: Optional[logging.Logger] = None):
        self._states: Dict[str, State] = {}
        self._transitions: Dict[Tuple[str, str], TransitionConfig] = {}
        self._current_state: Optional[str] = initial_state
        self._state_history: List[str] = []
        self._max_history: int = 100
        self._logger = logger or logging.getLogger(__name__)
        self._listeners: List[Callable[[str, str], None]] = []
        self._context: Dict[str, Any] = {}
        
    def get_transition(self, from_state: str, to_state: str) -> Optional[TransitionConfig]:
        """Get transition configuration between two states."""
        return self._transitions.get((from_state, to_state))
    
    @property
    def current_state(self) -> Optional[str]:
        """Get current state name."""
        return self._current_state
    
    @property
    def state_history(self) -> List[str]:
        """Get state transition history."""
        return self._state_history.copy()
    
    @property
    def available_transitions(self) -> List[str]:
        """Get list of states we can transition to from current state."""
        if not self._current_state:
            return []
        
        available = []
        for (from_state, to_state), config in self._transitions.items():
            if from_state == self._current_state and config.is_valid(self._context):
                available.append(to_state)
        return available
    
    def register_state(self, state: State) -> None:
        """Register a state in the machine."""
        if state.name in self._states:
            raise ValueError(f"State '{state.name}' already registered")
        self._states[state.name] = state
        self._logger.debug(f"Registered state: {state.name}")
    
    def register_transition(self, config: TransitionConfig) -> None:
        """Register a valid transition between states."""
        key = (config.from_state, config.to_state)
        
        # Validate states exist
        if config.from_state not in self._states:
            raise ValueError(f"From state '{config.from_state}' not registered")
        if config.to_state not in self._states:
            raise ValueError(f"To state '{config.to_state}' not registered")
        
        self._transitions[key] = config
        self._logger.debug(f"Registered transition: {config.from_state} -> {config.to_state}")
    
    def add_listener(self, listener: Callable[[str, str], None]) -> None:
        """Add a state change listener."""
        self._listeners.append(listener)
    
    def remove_listener(self, listener: Callable[[str, str], None]) -> None:
        """Remove a state change listener."""
        if listener in self._listeners:
            self._listeners.remove(listener)
    
    def update_context(self, **kwargs) -> None:
        """Update state machine context."""
        self._context.update(kwargs)
    
    def can_transition(self, to_state: str) -> bool:
        """Check if transition to target state is possible."""
        if not self._current_state:
            return False
        
        key = (self._current_state, to_state)
        if key not in self._transitions:
            return False
        
        config = self._transitions[key]
        return config.is_valid(self._context)
    
    def transition_to(self, to_state: str, force: bool = False) -> None:
        """
        Transition to a new state.
        
        Args:
            to_state: Target state name
            force: Force transition even if not configured
            
        Raises:
            TransitionError: If transition is not allowed
        """
        if not force and not self.can_transition(to_state):
            raise TransitionError(
                f"Cannot transition from '{self._current_state}' to '{to_state}'"
            )
        
        from_state = self._current_state
        
        # Exit current state
        if from_state and from_state in self._states:
            self._states[from_state].on_exit(self._context)
        
        # Execute transition action
        if from_state is not None:
            key = (from_state, to_state)
            if key in self._transitions:
                self._transitions[key].execute(self._context)
        
        # Enter new state
        self._current_state = to_state
        if to_state in self._states:
            self._states[to_state].on_enter(self._context)
        
        # Update history
        self._state_history.append(to_state)
        if len(self._state_history) > self._max_history:
            self._state_history.pop(0)
        
        # Notify listeners
        for listener in self._listeners:
            try:
                listener(from_state or "", to_state)
            except Exception as e:
                self._logger.error(f"Listener error: {e}")
        
        self._logger.info(f"Transitioned from '{from_state}' to '{to_state}'")
    
    @contextmanager
    def state_transaction(self):
        """
        Context manager for transactional state changes.
        Rolls back to original state on error.
        """
        original_state = self._current_state
        original_history = self._state_history.copy()
        
        try:
            yield self
        except Exception as e:
            # Rollback
            self._current_state = original_state
            self._state_history = original_history
            self._logger.error(f"State transaction failed, rolled back to '{original_state}': {e}")
            raise
    
    def reset(self, initial_state: Optional[str] = None) -> None:
        """Reset state machine to initial state."""
        self._current_state = initial_state
        self._state_history.clear()
        self._context.clear()
        self._logger.info(f"State machine reset to '{initial_state}'")
    
    def get_state_object(self, state_name: str) -> Optional[State]:
        """Get state object by name."""
        return self._states.get(state_name)
    
    def visualize(self) -> str:
        """Generate a text representation of the state machine."""
        lines = ["State Machine Visualization", "=" * 40]
        
        # Current state
        lines.append(f"Current State: {self._current_state or 'None'}")
        lines.append("")
        
        # States
        lines.append("States:")
        for state_name in sorted(self._states.keys()):
            marker = " *" if state_name == self._current_state else ""
            lines.append(f"  - {state_name}{marker}")
        lines.append("")
        
        # Transitions
        lines.append("Transitions:")
        for (from_state, to_state) in sorted(self._transitions.keys()):
            lines.append(f"  {from_state} -> {to_state}")
        
        return "\n".join(lines)

    def force_transition_to(self, to_state: str) -> None:
        """
        Force transition to state without validation or conditions.
        
        Args:
            to_state: Target state
        """
        if to_state not in self._states:
            raise ValueError(f"State {to_state} does not exist")
        
        from_state = self._current_state
        self._current_state = to_state
        
        # Trigger listeners
        for listener in self._listeners:
            try:
                listener(from_state or "UNKNOWN", to_state)
            except Exception as e:
                if hasattr(self, '_logger'):
                    self._logger.warning(f"Listener error: {e}")


class HierarchicalStateMachine(StateMachine):
    """State machine with support for nested states."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._parent_states: Dict[str, str] = {}
        self._child_states: Dict[str, Set[str]] = {}
    
    def register_nested_state(self, state: State, parent_state: str) -> None:
        """Register a state as child of another state."""
        self.register_state(state)
        
        if parent_state not in self._states:
            raise ValueError(f"Parent state '{parent_state}' not registered")
        
        self._parent_states[state.name] = parent_state
        
        if parent_state not in self._child_states:
            self._child_states[parent_state] = set()
        self._child_states[parent_state].add(state.name)
    
    def get_parent_state(self, state_name: str) -> Optional[str]:
        """Get parent state of a nested state."""
        return self._parent_states.get(state_name)
    
    def get_child_states(self, state_name: str) -> Set[str]:
        """Get child states of a parent state."""
        return self._child_states.get(state_name, set()).copy()
    
    def is_in_state(self, state_name: str, check_nested: bool = True) -> bool:
        """
        Check if currently in a state or its parent states.
        
        Args:
            state_name: State to check
            check_nested: Also check parent states
        """
        if self._current_state == state_name:
            return True
        
        if check_nested and self._current_state:
            # Check if current state is a child of the queried state
            current = self._current_state
            while current in self._parent_states:
                current = self._parent_states[current]
                if current == state_name:
                    return True
        
        return False


# Concrete state implementations for common use cases

class SimpleState(State):
    """Simple state implementation."""
    
    def __init__(self, name: str, metadata: Optional[Dict[str, Any]] = None):
        self._name = name
        self._metadata = metadata or {}
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def metadata(self) -> Dict[str, Any]:
        return self._metadata


class ConditionalState(State):
    """State with entry/exit conditions."""
    
    def __init__(
        self,
        name: str,
        entry_condition: Optional[Callable[[Dict[str, Any]], bool]] = None,
        exit_condition: Optional[Callable[[Dict[str, Any]], bool]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
        self._name = name
        self._entry_condition = entry_condition
        self._exit_condition = exit_condition
        self._metadata = metadata or {}
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def metadata(self) -> Dict[str, Any]:
        return self._metadata
    
    def on_enter(self, context: Dict[str, Any]) -> None:
        if self._entry_condition and not self._entry_condition(context):
            raise TransitionError(f"Entry condition failed for state '{self.name}'")
    
    def on_exit(self, context: Dict[str, Any]) -> None:
        if self._exit_condition and not self._exit_condition(context):
            raise TransitionError(f"Exit condition failed for state '{self.name}'")


class TimedState(State):
    """State with timeout capability."""
    
    def __init__(
        self,
        name: str,
        timeout: float,
        timeout_state: str,
        metadata: Optional[Dict[str, Any]] = None
    ):
        self._name = name
        self._timeout = timeout
        self._timeout_state = timeout_state
        self._metadata = metadata or {}
        self._enter_time: Optional[float] = None
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def metadata(self) -> Dict[str, Any]:
        return self._metadata
    
    def on_enter(self, context: Dict[str, Any]) -> None:
        self._enter_time = time.time()
        context['_timed_state_enter'] = self._enter_time
        context['_timed_state_timeout'] = self._timeout
        context['_timed_state_timeout_target'] = self._timeout_state
    
    def is_timed_out(self) -> bool:
        """Check if state has timed out."""
        if self._enter_time is None:
            return False
        return (time.time() - self._enter_time) > self._timeout