"""
Component: Persistent Storage and State Machine
Description: Manages write-ahead logs and the active key-value state machine storage engine.
Lead Engineer: Syed Saad Bin Irfan
"""

from typing import List, Dict

class WriteAheadLogStorage:
    """Manages the write-ahead consensus log history and applies committed updates to the state machine."""
    
    def __init__(self) -> None:
        self.entries_log: List[Dict[str, any]] = []
        self.state_machine_data: Dict[str, str] = {}

    def append_entry(self, term: int, command: str) -> int:
        """Appends an uncommitted command packet to the local log and returns its index coordinate."""
        entry = {"term": term, "command": command}
        self.entries_log.append(entry)
        return len(self.entries_log) - 1

    def apply_to_state_machine(self, log_index: int) -> None:
        """Executes a confirmed, committed log command into the permanent state machine storage."""
        if log_index < len(self.entries_log):
            command_str = self.entries_log[log_index]["command"]
            if "SET" in command_str:
                parts = command_str.replace("SET ", "").split("=")
                if len(parts) == 2:
                    key = parts[0].strip()
                    value = parts[1].strip()
                    self.state_machine_data[key] = value