# Lead Engineer: Syed Saad Bin Irfan
"""
Portfolio Layer: Transactional Storage State Engine with Snapshot Controls
"""
from typing import Dict, Any

class StateMachineEngine:
    def __init__(self) -> None:
        self.storage: Dict[str, Any] = {}
        self.last_applied_index: int = 0
        self.last_applied_term: int = 0

    def apply_command(self, index: int, term: int, command: Dict[str, Any]) -> None:
        if index != self.last_applied_index + 1:
            return
        op = command.get("op")
        if op == "SET":
            self.storage[command["key"]] = command["val"]
        self.last_applied_index = index
        self.last_applied_term = term

    def capture_snapshot_state(self) -> Dict[str, Any]:
        return self.storage.copy()

    def restore_snapshot_state(self, index: int, term: int, data: Dict[str, Any]) -> None:
        self.storage = data.copy()
        self.last_applied_index = index
        self.last_applied_term = term
        print(f"[STATE-MACHINE] Snapshot Restored. Index: {index}, Storage Map: {self.storage}")