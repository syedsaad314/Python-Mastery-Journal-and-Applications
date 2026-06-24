# Lead Engineer: Syed Saad Bin Irfan
"""
Portfolio Layer: System State and Core Schema Models
"""
from typing import Dict, Any

class StateSnapshotImage:
    def __init__(self, last_index: int, last_term: int, database_payload: Dict[str, str]) -> None:
        self.last_index = last_index
        self.last_term = last_term
        self.database_payload = database_payload

    def compile_structural_packet(self) -> Dict[str, Any]:
        return {
            "metadata": {
                "last_included_index": self.last_index,
                "last_included_term": self.last_term
            },
            "state": self.database_payload
        }