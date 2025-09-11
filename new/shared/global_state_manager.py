"""
Global State Manager Module
Manages global application state and navigation across multiple workflows (copy, fax, scan, etc.)
"""

from typing import Dict, Optional, Any, Set, List, Deque
import logging
from enum import Enum
from dataclasses import dataclass
from pathlib import Path
from collections import deque

from .state_machine import StateMachine, State
from .config_generator import ConfigGenerator
from dunetuf.ui.new.shared.enums import Feature

@dataclass
class FeatureContext:
    """Context information for a feature."""
    name: str
    current_state: Optional[str] = None
    state_machine: Optional[StateMachine] = None
    config_generator: Optional[ConfigGenerator] = None
    metadata: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class GlobalStateManager:
    """
    Manages global application state across multiple features.
    Tracks current feature and provides centralized navigation to HOME.
    """
    
    def __init__(self, logger: Optional[logging.Logger] = None):
        """
        Initialize Global State Manager.
        
        Args:
            logger: Logger instance
        """
        self._logger = logger or logging.getLogger(__name__)
        
        # Feature management
        self._current_feature: Optional[Feature] = None
        self._feature_contexts: Dict[Feature, FeatureContext] = {}
        self._home_navigation_handlers: Dict[Feature, Any] = {}
        
        # Global state tracking
        self._global_state_history: List[str] = []
        self._max_history: int = 50
        
        # Home state identification
        self._home_states: Set[str] = {"HOME", "MAIN_HOME", "HOME_SCREEN"}
        
        # Path finding configuration
        self._max_path_depth: int = 10  # Maximum steps to find HOME
        self._path_cache: Dict[str, Optional[List[str]]] = {}  # Cache for performance

        # Register HOME feature by default (no state machine, no navigation handler)
        self._register_default_home_feature()
        
        self._logger.info("GlobalStateManager initialized")

    def _register_default_home_feature(self) -> None:
        """Register HOME feature by default without state machine or navigation handler."""
        home_context = FeatureContext(
            name=Feature.HOME.value,
            current_state="HOME",  # HOME feature is always in HOME state
            state_machine=None,     # No state machine for HOME
            config_generator=None,  # No config generator for HOME
            metadata={
                "is_default": True,
                "description": "Default HOME feature - always available",
                "can_exit_to_home": True,  # HOME can always "exit" to itself
                "registered_automatically": True
            }
        )
        
        self._feature_contexts[Feature.HOME] = home_context
        self._logger.debug("HOME feature registered by default")
    
    def register_feature(
        self,
        feature: Feature,
        state_machine: StateMachine,
        config_generator: Optional[ConfigGenerator] = None,
        navigation_handler: Optional[Any] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Register a feature with its state machine and navigation handler.
        
        Args:
            feature: Application feature
            state_machine: State machine for the feature
            config_generator: Configuration generator for the feature
            navigation_handler: Navigation handler for the feature
            metadata: Additional metadata for the feature
        """
        if feature == Feature.HOME:
            self._logger.warning("HOME feature is registered by default and cannot be overridden")
            return
    
        context = FeatureContext(
            name=feature.value,
            state_machine=state_machine,
            config_generator=config_generator,
            metadata=metadata or {}
        )
        
        self._feature_contexts[feature] = context
        
        if navigation_handler:
            self._home_navigation_handlers[feature] = navigation_handler
        
        # Add state change listener to track feature states
        state_machine.add_listener(self._on_feature_state_change)
        
        self._logger.info(f"Registered feature: {feature.value}")
    
    def set_current_feature(self, feature: Feature) -> None:
        """
        Set the current active feature.
        
        Args:
            feature: Feature to set as current
            
        Raises:
            ValueError: If feature is not registered
        """
        if feature not in self._feature_contexts:
            raise ValueError(f"Feature {feature.value} is not registered")
        
        previous_feature = self._current_feature
        self._current_feature = feature
        
        # Get context for all features (including HOME)
        context = self._feature_contexts[feature]
        
        # Update current state from feature's state machine (except for HOME)
        if feature == Feature.HOME:
            # HOME feature always stays in HOME state
            context.current_state = "HOME"
        elif context.state_machine:
            context.current_state = context.state_machine.current_state
        
        self._logger.info(f"Current feature changed from {previous_feature} to {feature.value}")
        
        # Record in history
        self._add_to_history(f"{feature.value}:{context.current_state or 'UNKNOWN'}")
    
    def get_current_feature(self) -> Optional[Feature]:
        """Get the current active feature."""
        return self._current_feature
    
    def get_current_state(self) -> Optional[str]:
        """Get the current state of the active feature."""
        if not self._current_feature:
            return None
        
        context = self._feature_contexts.get(self._current_feature)
        if not context:
            return None
        
        return context.current_state
    
    def get_full_current_state(self) -> str:
        """Get full current state information."""
        if not self._current_feature:
            return "UNKNOWN:UNKNOWN"
        
        current_state = self.get_current_state()
        return f"{self._current_feature.value}:{current_state or 'UNKNOWN'}"
    
    def is_at_home(self) -> bool:
        """
        Check if currently at any HOME state.
        
        Returns:
            bool: True if at home state
        """
        if self._current_feature == Feature.HOME:
            return True
        
        current_state = self.get_current_state()
        if current_state and current_state in self._home_states:
            return True
        
        # Check if current state has home-like metadata
        if self._current_feature:
            context = self._feature_contexts.get(self._current_feature)
            if context and context.state_machine:
                state_obj = context.state_machine.get_state_object(current_state or "")
                if state_obj and state_obj.metadata.get("can_exit_to_home"):
                    return False  # Has exit to home capability but not at home
        
        return False
    
    def can_exit_to_home(self) -> bool:
        """
        Check if current state can exit to home using multi-step path finding.
        
        Returns:
            bool: True if can exit to home (directly or through multiple steps)
        """
        if self.is_at_home():
            return True
        
        if not self._current_feature:
            return False
        
        context = self._feature_contexts.get(self._current_feature)
        if not context or not context.state_machine:
            return False
        
        current_state = context.current_state
        if not current_state:
            return False
        
        # Find path to home using BFS
        path = self._find_path_to_home(context.state_machine, current_state)
        return path is not None
    
    def get_navigation_path_to_home(self) -> List[str]:
        """
        Get the navigation path to HOME from current state using multi-step path finding.
        
        Returns:
            List[str]: List of states in navigation path (empty if no path or already at home)
        """
        if self.is_at_home():
            return []
        
        if not self._current_feature:
            return []
        
        context = self._feature_contexts.get(self._current_feature)
        if not context or not context.state_machine:
            return []
        
        current_state = context.current_state
        if not current_state:
            return []
        
        # Find complete path using BFS
        path = self._find_path_to_home(context.state_machine, current_state)
        return path if path is not None else []
    
    def _find_path_to_home(
        self, 
        state_machine: StateMachine, 
        start_state: str
    ) -> Optional[List[str]]:
        """
        Find path from start_state to any HOME state using BFS (Breadth-First Search).
        
        Args:
            state_machine: State machine to search in
            start_state: Starting state for path finding
            
        Returns:
            List[str]: Path to home (excluding start_state) or None if no path found
        """
        # Check cache first
        cache_key = f"{id(state_machine)}:{start_state}"
        if cache_key in self._path_cache:
            cached_result = self._path_cache[cache_key]
            self._logger.debug(f"Path cache hit for {start_state}: {cached_result}")
            return cached_result
        
        # Check if start state is already a home state
        if start_state in self._home_states:
            self._path_cache[cache_key] = []
            return []
        
        # BFS implementation
        queue: Deque[tuple[str, List[str]]] = deque([(start_state, [])])
        visited: Set[str] = {start_state}
        
        self._logger.debug(f"Starting BFS path finding from {start_state} to HOME")
        
        while queue:
            current_state, path = queue.popleft()
            
            # Prevent infinite loops with depth limit
            if len(path) >= self._max_path_depth:
                self._logger.debug(f"Path depth limit reached ({self._max_path_depth}) for {start_state}")
                continue
            
            # Get available transitions from current state
            available_transitions = self._get_transitions_from_state(state_machine, current_state)
            
            for next_state in available_transitions:
                if next_state in visited:
                    continue
                
                new_path = path + [next_state]
                
                # Check if we reached a home state
                if next_state in self._home_states:
                    self._logger.debug(f"Found path to HOME: {start_state} -> {' -> '.join(new_path)}")
                    self._path_cache[cache_key] = new_path
                    return new_path
                
                # Check if next state has explicit home exit capability
                state_obj = state_machine.get_state_object(next_state)
                if state_obj and state_obj.metadata.get("can_exit_to_home"):
                    # This state can directly exit to home, so we found a valid path
                    self._logger.debug(f"Found path to HOME via can_exit_to_home state: {start_state} -> {' -> '.join(new_path)}")
                    self._path_cache[cache_key] = new_path
                    return new_path
                
                # Add to queue for further exploration
                queue.append((next_state, new_path))
                visited.add(next_state)
        
        # No path found
        self._logger.debug(f"No path to HOME found from {start_state}")
        self._path_cache[cache_key] = None
        return None
    
    def _get_transitions_from_state(
        self, 
        state_machine: StateMachine, 
        from_state: str
    ) -> List[str]:
        """
        Get all possible transition destinations from a given state.
        
        Args:
            state_machine: State machine to query
            from_state: Source state
            
        Returns:
            List[str]: List of destination states accessible from from_state
        """
        transitions = []
        
        # Get all registered transitions
        if hasattr(state_machine, '_transitions'):
            for transition in state_machine._transitions:
                # Handle transition as tuple (from_state, to_state)
                if isinstance(transition, tuple) and len(transition) >= 2:
                    if transition[0] == from_state:
                        transitions.append(transition[1])
                # Handle transition as object with attributes
                elif hasattr(transition, 'from_state') and transition.from_state == from_state:
                    if hasattr(transition, 'to_state'):
                        transitions.append(transition.to_state)
        
        # Fallback: use available_transitions property directly
        elif hasattr(state_machine, 'available_transitions'):
            # Temporarily set state to get available transitions
            original_state = state_machine.current_state
            try:
                state_machine._current_state = from_state
                transitions = list(state_machine.available_transitions)
            finally:
                state_machine._current_state = original_state
        
        self._logger.debug(f"Transitions from {from_state}: {transitions}")
        return transitions
    
    def clear_path_cache(self) -> None:
        """Clear the path finding cache. Useful when state machine configuration changes."""
        self._path_cache.clear()
        self._logger.debug("Path finding cache cleared")
    
    def navigate_to_home(self) -> bool:
        """
        Navigate to HOME from current location using multi-step navigation.
        
        Returns:
            bool: True if navigation successful
            
        Raises:
            RuntimeError: If navigation is not possible
        """
        if self.is_at_home():
            self._logger.info("Already at HOME")
            return True
        
        if not self.can_exit_to_home():
            raise RuntimeError("Cannot exit to HOME from current state")
        
        self._logger.info(f"Navigating to HOME from {self.get_full_current_state()}")
        
        try:
            # Get the navigation path
            navigation_path = self.get_navigation_path_to_home()
            if not navigation_path:
                raise RuntimeError("No navigation path to HOME found")
            
            self._logger.info(f"Using navigation path: {' -> '.join(navigation_path)}")
            
            # Execute multi-step navigation
            success = self._execute_navigation_path(navigation_path)
            
            if success:
                self._logger.info("Successfully navigated to HOME")
                #TODO: CHANGE
                # Update global state to HOME feature if we reached a home state
                if navigation_path and navigation_path[-1] in self._home_states:
                    self.set_current_feature(Feature.HOME)
            else:
                self._logger.error("Failed to complete navigation to HOME")
            
            return success
            
        except Exception as e:
            self._logger.error(f"Failed to navigate to HOME: {e}")
            raise
    
    def _execute_navigation_path(self, path: List[str]) -> bool:
        """
        Execute a multi-step navigation path.
        
        Args:
            path: List of states to navigate through
            
        Returns:
            bool: True if navigation successful
        """
        if not self._current_feature:
            return False
        
        context = self._feature_contexts.get(self._current_feature)
        if not context or not context.state_machine:
            return False
        
        try:
            # Try to use feature-specific navigation handler for each step
            if self._current_feature in self._home_navigation_handlers:
                handler = self._home_navigation_handlers[self._current_feature]
                
                for i, target_state in enumerate(path):
                    self._logger.debug(f"Navigation step {i+1}/{len(path)}: -> {target_state}")
                    
                    if hasattr(handler, 'navigate_to'):
                        handler.navigate_to(target_state)
                    else:
                        # Fallback to direct state machine navigation
                        context.state_machine.transition_to(target_state)
                    
                    # Update current state
                    context.current_state = target_state
                    self._add_to_history(f"NAV_STEP:{self._current_feature.value}:{target_state}")
                
                return True
            
            # Fallback: direct state machine navigation for entire path
            for i, target_state in enumerate(path):
                self._logger.debug(f"Direct navigation step {i+1}/{len(path)}: -> {target_state}")
                context.state_machine.transition_to(target_state)
                context.current_state = target_state
                self._add_to_history(f"DIRECT_NAV_STEP:{self._current_feature.value}:{target_state}")
            
            return True
            
        except Exception as e:
            self._logger.error(f"Navigation path execution failed at step: {e}")
            return False
    
    def get_path_finding_stats(self) -> Dict[str, Any]:
        """
        Get statistics about path finding performance.
        
        Returns:
            Dict with path finding statistics
        """
        return {
            "cache_size": len(self._path_cache),
            "max_path_depth": self._max_path_depth,
            "cached_paths": {
                key: "PATH_FOUND" if value is not None else "NO_PATH"
                for key, value in self._path_cache.items()
            }
        }
    
    def get_state_history(self) -> List[str]:
        """Get global state history."""
        return self._global_state_history.copy()
    
    def get_feature_info(self, feature: Feature) -> Optional[Dict[str, Any]]:
        """
        Get information about a registered feature.
        
        Args:
            feature: Feature to get info for
            
        Returns:
            Dict with feature information or None if not registered
        """
        if feature not in self._feature_contexts:
            return None
        
        context = self._feature_contexts[feature]

        # Special handling for HOME feature
        if feature == Feature.HOME:
            return {
                "name": context.name,
                "current_state": context.current_state,
                "has_state_machine": False,  # HOME never has state machine
                "has_config_generator": False,  # HOME never has config generator
                "has_navigation_handler": False,  # HOME never has navigation handler
                "metadata": context.metadata,
                "can_exit_to_home": True,  # HOME can always "exit" to itself
                "is_default_feature": True
            }
        return {
            "name": context.name,
            "current_state": context.current_state,
            "has_state_machine": context.state_machine is not None,
            "has_config_generator": context.config_generator is not None,
            "has_navigation_handler": feature in self._home_navigation_handlers,
            "metadata": context.metadata,
            "can_exit_to_home": self._can_feature_exit_to_home(feature)
        }
    
    def export_status_report(self) -> Dict[str, Any]:
        """
        Export comprehensive status report.
        
        Returns:
            Dict with complete status information
        """
        return {
            "current_feature": self._current_feature.value if self._current_feature else None,
            "current_state": self.get_current_state(),
            "full_current_state": self.get_full_current_state(),
            "is_at_home": self.is_at_home(),
            "can_exit_to_home": self.can_exit_to_home(),
            "registered_features": [f.value for f in self._feature_contexts.keys()],
            "navigation_path_to_home": self.get_navigation_path_to_home(),
            "state_history": self._global_state_history[-10:],  # Last 10 entries
            "features_info": {
                f.value: self.get_feature_info(f) 
                for f in self._feature_contexts.keys()
            }
        }
    
    def _on_feature_state_change(self, from_state: str, to_state: str) -> None:
        """Handle state changes from feature state machines."""
        if self._current_feature:
            context = self._feature_contexts.get(self._current_feature)
            if context:
                context.current_state = to_state
                self._add_to_history(f"{self._current_feature.value}:{to_state}")
                self._logger.debug(f"Feature {self._current_feature.value} state: {from_state} -> {to_state}")
    
    def _find_home_target_state(self, state_machine: StateMachine) -> Optional[str]:
        """Find the best HOME target state in the state machine."""
        # First, look for explicit HOME states
        for home_state in self._home_states:
            if home_state in state_machine._states:
                return home_state
        
        # Then, look for states that can exit to home
        for state_name, state_obj in state_machine._states.items():
            if state_obj.metadata.get("can_exit_to_home"):
                return state_name
        
        return None
    
    def _can_feature_exit_to_home(self, feature: Feature) -> bool:
        """Check if a feature can exit to home."""
        if feature == Feature.HOME:
            return True
        
        context = self._feature_contexts.get(feature)
        if not context or not context.state_machine:
            return False
        
        return self._find_home_target_state(context.state_machine) is not None
    
    def _add_to_history(self, entry: str) -> None:
        """Add entry to global history."""
        self._global_state_history.append(entry)
        if len(self._global_state_history) > self._max_history:
            self._global_state_history.pop(0)


# Singleton instance
_global_state_manager: Optional[GlobalStateManager] = None


def get_global_state_manager() -> GlobalStateManager:
    """Get the global state manager singleton."""
    global _global_state_manager
    if _global_state_manager is None:
        _global_state_manager = GlobalStateManager()
    return _global_state_manager


def initialize_global_state_manager(logger: Optional[logging.Logger] = None) -> GlobalStateManager:
    """Initialize and get the global state manager."""
    global _global_state_manager
    _global_state_manager = GlobalStateManager(logger)
    return _global_state_manager