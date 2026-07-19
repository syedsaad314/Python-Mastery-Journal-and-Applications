# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Event Store to Transactional Outbox Bridge
Description: Links an append-only event stream directly to an outbox buffer to ensure 
             downstream microservices stay updated automatically.
"""
from typing import List, Dict

class EventStoreOutboxBridge:
    def __init__(self) -> None:
        self.append_only_log: List[dict] = []
        self.outbox_buffer: List[dict] = []

    def commit_transactional_change(self, aggregate_id: str, change_event: dict) -> None:
        # Atomic change block updating both the event store history log and outbox publisher table
        self.append_only_log.append({"id": aggregate_id, "event": change_event})
        self.outbox_buffer.append({"delivered": False, "event": change_event})

    def process_outbox_queue(self) -> int:
        published_count = 0
        for item in self.outbox_buffer:
            if not item["delivered"]:
                item["delivered"] = True
                published_count += 1
        return published_count

if __name__ == "__main__":
    bridge = EventStoreOutboxBridge()
    bridge.commit_transactional_change("user_101", {"type": "BALANCE_INCREASED", "val": 100})
    
    flushed = bridge.process_outbox_queue()
    assert flushed == 1
    assert bridge.outbox_buffer[0]["delivered"] is True
    print(f"[BRIDGE SYNCED] Event log successfully bound to atomic outbox table. Flushed messages: {flushed}")