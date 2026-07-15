# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Transactional Outbox Buffer
Description: Implements an atomic outbox queue that pairs local database state 
             mutations with event staging logs to prevent split-brain anomalies.
"""
from typing import List, Dict, Any

class TransactionalOutboxBuffer:
    def __init__(self) -> None:
        self.mock_database_table: Dict[str, Any] = {}
        self.outbox_table: List[Dict[str, Any]] = []

    def execute_atomic_write(self, entity_id: str, state_update: dict, event_payload: dict) -> None:
        # Simulate an ACID database transaction block updating the table and outbox simultaneously
        self.mock_database_table[entity_id] = state_update
        
        self.outbox_table.append({
            "id": len(self.outbox_table) + 1,
            "processed": False,
            "payload": event_payload
        })

    def sweep_pending_outbox_events(self) -> List[Dict[str, Any]]:
        return [msg for msg in self.outbox_table if not msg["processed"]]

if __name__ == "__main__":
    buffer = TransactionalOutboxBuffer()
    buffer.execute_atomic_write(
        entity_id="order_88", 
        state_update={"status": "SAVED"}, 
        event_payload={"evt": "ORDER_CREATED", "id": "order_88"}
    )
    
    pending = buffer.sweep_pending_outbox_events()
    assert len(pending) == 1
    assert buffer.mock_database_table["order_88"] == {"status": "SAVED"}