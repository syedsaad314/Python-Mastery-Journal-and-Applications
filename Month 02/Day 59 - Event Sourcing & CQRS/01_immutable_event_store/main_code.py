# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Immutable Event Store Log
Description: Implements an append-only transactional log stream enforcing 
             strict immutability on domain deltas.
"""
from dataclasses import dataclass
from typing import List, Dict
import time

@dataclass(frozen=True)
class EventRecord:
    aggregate_id: str
    version: int
    event_type: str
    payload: dict
    timestamp: float = time.time()

class AppendOnlyEventStore:
    def __init__(self) -> None:
        self._streams: Dict[str, List[EventRecord]] = {}

    def append_to_stream(self, aggregate_id: str, expected_version: int, event_type: str, payload: dict) -> None:
        stream = self._streams.setdefault(aggregate_id, [])
        current_version = len(stream)
        
        if current_version != expected_version:
            raise ValueError(f"[CONCURRENCY ERROR] Optimistic lock crash! Stream version is {current_version}, expected {expected_version}")
            
        record = EventRecord(aggregate_id, current_version + 1, event_type, payload)
        stream.append(record)

    def read_stream(self, aggregate_id: str) -> List[EventRecord]:
        return self._streams.get(aggregate_id, []).copy()

if __name__ == "__main__":
    store = AppendOnlyEventStore()
    store.append_to_stream("acc_01", 0, "ACCOUNT_OPENED", {"holder": "Saad", "initial": 500})
    store.append_to_stream("acc_01", 1, "FUNDS_DEPOSITED", {"amount": 250})
    
    events = store.read_stream("acc_01")
    assert len(events) == 2
    print(f"[STORE CONFIRMED] Stream initialized. Current structural version check: {events[-1].version}")