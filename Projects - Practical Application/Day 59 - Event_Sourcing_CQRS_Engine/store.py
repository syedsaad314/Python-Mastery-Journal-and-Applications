# Lead Engineer: Syed Saad Bin Irfan
"""
Portfolio Layer: Append-Only Event Store with Integrated Snapshot Engine
"""
from typing import Dict, List, Tuple, Optional
from models import TransactionDomainEvent

class EventStoreEngine:
    def __init__(self) -> None:
        self._streams: Dict[str, List[TransactionDomainEvent]] = {}
        self._snapshots: Dict[str, Tuple[int, dict]] = {} # Maps aggregate_id -> (version, state)

    def append_events(self, aggregate_id: str, current_version: int, new_events: List[dict]) -> List[TransactionDomainEvent]:
        stream = self._streams.setdefault(aggregate_id, [])
        
        # Concurrency verification checks
        if len(stream) != current_version:
            raise RuntimeError(f"Concurrency Collision: Expected version {current_version}, found {len(stream)}")
            
        allocated_records = []
        next_version = current_version
        
        for entry in new_events:
            next_version += 1
            record = TransactionDomainEvent(
                aggregate_id=aggregate_id,
                version=next_version,
                event_type=entry["type"],
                payload=entry["payload"]
            )
            stream.append(record)
            allocated_records.append(record)
            
        return allocated_records

    def save_snapshot(self, aggregate_id: str, version: int, state: dict) -> None:
        self._snapshots[aggregate_id] = (version, state.copy())

    def load_snapshot(self, aggregate_id: str) -> Tuple[int, dict]:
        return self._snapshots.get(aggregate_id, (0, {"balance": 0.0, "status": "UNINITIALIZED"}))

    def read_stream_mutations(self, aggregate_id: str, starting_version: int) -> List[TransactionDomainEvent]:
        all_events = self._streams.get(aggregate_id, [])
        return [evt for evt in all_events if evt.version > starting_version]