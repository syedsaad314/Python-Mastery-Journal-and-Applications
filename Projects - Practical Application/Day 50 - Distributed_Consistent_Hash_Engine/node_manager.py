# Lead Engineer: Syed Saad Bin Irfan
"""
Portfolio Layer: In-Memory Key-Value Node Mock Engine
"""
from typing import Dict, Any

class VirtualDataNodeStorage:
    def __init__(self, node_id: str) -> None:
        self.node_id = node_id
        self.local_vault: Dict[str, str] = {}

    def save_record(self, key: str, value: str) -> None:
        self.local_vault[key] = value

    def purge_record(self, key: str) -> None:
        self.local_vault.pop(key, None)