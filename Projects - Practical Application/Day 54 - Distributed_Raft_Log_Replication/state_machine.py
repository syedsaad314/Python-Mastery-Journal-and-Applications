# Lead Engineer: Syed Saad Bin Irfan
"""
Portfolio Layer: Key-Value Storage Application State Container
"""
from typing import Dict, Any

class StateMachineEngine:
    def __init__(self) -> None:
        self.storage: Dict[str, Any] = {}
        self.last_applied_index: int = 0

    def apply_command(self, index: int, command: Dict[str, Any]) -> None:
        if index != self.last_applied_index + 1:
            # Enforce sequential application safety rules
            return
            
        op = command.get("op")
        if op == "SET":
            self.storage[command["key"]] = command["val"]
        elif op == "DEL":
            self.storage.pop(command["key"], None)
            
        self.last_applied_index = index
        print(f"[STATE-MACHINE] Applied entry index {index}. Current Storage Map: {self.storage}")