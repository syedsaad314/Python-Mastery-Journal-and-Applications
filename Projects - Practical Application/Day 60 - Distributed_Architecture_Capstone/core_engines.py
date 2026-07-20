# Lead Engineer: Syed Saad Bin Irfan
"""
Portfolio Layer: Combined Architectural Layout Models for Simulation Testing
"""
import asyncio
from typing import List, Dict, Tuple
from models import UnifiedCapstoneEvent

class CapstoneEventStoreAndOutbox:
    def __init__(self) -> None:
        self.write_stream: List[UnifiedCapstoneEvent] = []
        self.outbox_buffer: List[dict] = []
        self.snapshot_registry: Dict[str, Tuple[int, dict]] = {}
        self.stream_version = 0

    def append_with_occ(self, aggregate_id: str, expected_ver: int, etype: str, data: dict) -> UnifiedCapstoneEvent:
        # Strict Optimistic Concurrency Control (OCC) lock validation check
        if self.stream_version != expected_ver:
            raise RuntimeError(f"OCC Crash! Version mismatch. Stream: {self.stream_version}, Client expected: {expected_ver}")
            
        self.stream_version += 1
        evt = UnifiedCapstoneEvent(correlation_id=uuid.uuid4(), event_type=etype, payload=data) # type: ignore
        
        # Atomic Write: Commit to historical record stream and staging outbox at the exact same instant
        self.write_stream.append(evt)
        self.outbox_buffer.append({"processed": False, "event": evt})
        return evt

    def save_snapshot_checkpoint(self, aggregate_id: str, state: dict) -> None:
        self.snapshot_registry[aggregate_id] = (self.stream_version, state.copy())


class OrchestratedSagaComponent:
    def __init__(self) -> None:
        self.state_log: List[str] = []

    async def execute_forward_chain(self, fail_downstream: bool) -> bool:
        self.state_log.append("RESERVED_STOCK")
        if fail_downstream:
            print("   [FAULT TRIGGER] Orchestrator caught a downstream microservice failure! Starting rollback...")
            await self.execute_backward_rollback()
            return False
        self.state_log.append("COMPLETED_CHARGE")
        return True

    async def execute_backward_rollback(self) -> None:
        # Reverse processing sequence cleanup loop
        while self.state_log:
            step = self.state_log.pop()
            print(f"      -> [ORCHESTRATOR CLEANUP] Reversing step: {step}")


class ChoreographedSagaComponent:
    def __init__(self) -> None:
        self.local_db_state = "STABLE"

    async def handle_incoming_failure_signal(self, event: UnifiedCapstoneEvent) -> None:
        if event.event_type == "TRANSACTION_CRASHED_EVENT":
            print(f"   [CHOREOGRAPHY LISTEN] Autonomous component caught failure token {event.event_id[:6] if isinstance(event.event_id, str) else 'TOKEN'}. Running local rollback...")
            self.local_db_state = "RESTORED_COMPENSATION_STATE"