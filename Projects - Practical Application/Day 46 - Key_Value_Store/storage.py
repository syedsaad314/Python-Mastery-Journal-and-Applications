# Lead Engineer: Syed Saad Bin Irfan
"""
Component: Node Storage and State Machine
Description: Manages a node's local log sequence and applies committed records to memory.
"""

from typing import List, Dict
from models import LogEntry

class LocalLogStore:
    def __init__(self) -> None:
        self.history: List[LogEntry] = []
        self.memory_state: Dict[str, str] = {}

    def force_override_history(self, clean_history: List[LogEntry]) -> None:
        self.history = clean_history

    def append_raw_entry(self, term: int, command: str) -> None:
        self.history.append(LogEntry(term, command))

    def rebuild_state_machine(self, commit_index: int) -> None:
        """Re-evaluates log history up to the commit index boundary to guarantee state consistency."""
        self.memory_state.clear()
        for idx in range(0, commit_index + 1):
            if idx < len(self.history):
                cmd_str = self.history[idx].command
                if "SET" in cmd_str:
                    parts = cmd_str.replace("SET ", "").split("=")
                    if len(parts) == 2:
                        self.memory_state[parts[0].strip()] = parts[1].strip()