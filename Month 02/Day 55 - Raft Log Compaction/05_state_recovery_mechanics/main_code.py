# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Node Boot Recovery Mechanics
Description: Restores a node's key-value store and tracking pointers from a 
             saved snapshot after a crash or reboot.
"""
from typing import Dict, Any

class ResilientStateMachine:
    def __init__(self) -> None:
        self.kv_store: Dict[str, Any] = {}
        self.last_applied_index = 0

    def recover_from_disk_image(self, backup_file_image: Dict[str, Any]) -> None:
        self.last_applied_index = backup_file_image["last_included_index"]
        self.kv_store = backup_file_image["state_data"].copy()

if __name__ == "__main__":
    machine = ResilientStateMachine()
    mock_disk_file = {
        "last_included_index": 82,
        "state_data": {"api_key": "secured_token", "nodes": 3}
    }
    machine.recover_from_disk_image(mock_disk_file)
    assert machine.last_applied_index == 82
    assert machine.kv_store["api_key"] == "secured_token"