# Lead Engineer: Syed Saad Bin Irfan
"""
Portfolio Layer: Idempotent Client Session Database Caches
"""
from typing import Dict, Any

class IdempotentSessionStore:
    def __init__(self) -> None:
        # Mapping: client_id -> sequence_id -> response_payload
        self.vault: Dict[str, Dict[int, Any]] = {}

    def fetch_cached_response(self, client_id: str, sequence_id: int) -> Any:
        if client_id in self.vault and sequence_id in self.vault[client_id]:
            return self.vault[client_id][sequence_id]
        return None

    def cache_session_transaction(self, client_id: str, sequence_id: int, response: Any) -> None:
        if client_id not in self.vault:
            self.vault[client_id] = {}
        self.vault[client_id][sequence_id] = response