"""
Core Topic: Transactional Outbox Pattern
Description: Guarantees reliable event publishing by saving events to a local outbox database table.
Lead Engineer: Syed Saad Bin Irfan
"""

from typing import List, Dict, Any

class MockDatabaseConnection:
    """Simulates an isolated relational database supporting atomic operations."""
    
    def __init__(self) -> None:
        self.business_records: Dict[str, Any] = {}
        self.outbox_table: List[Dict[str, Any]] = []

    def commit_atomic_dual_write(self, entity_id: str, data: str, outbound_event: dict) -> None:
        """Guarantees atomicity by updating business records and writing to the outbox in one transaction."""
        # 1. Update the local business entity
        self.business_records[entity_id] = data
        
        # 2. Append the tracking event to the outbox table within the same transaction scope
        self.outbox_table.append({
            "id": len(self.outbox_table) + 1,
            "payload": outbound_event,
            "dispatched": False
        })


if __name__ == "__main__":
    db = MockDatabaseConnection()
    
    event_payload = {"event": "USER_UPGRADED", "target": "saad_irfan", "tier": "PRO"}
    
    # Execute an atomic dual-write operation
    db.commit_atomic_dual_write("user-102", "STATUS_ACTIVE", event_payload)
    
    print(f"[OUTBOX-DB] Internal Business State Table: {db.business_records}")
    print(f"[OUTBOX-DB] Outbox Message Log Table: {db.outbox_table}")