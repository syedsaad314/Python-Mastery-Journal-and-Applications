# Lead Engineer: Syed Saad Bin Irfan
"""
Portfolio Layer: Autonomous Decoupled Services with Built-In Outbox and Deduplication Guards
"""
import asyncio
from typing import Dict, List, Any, Set
from models import ChoreographyEvent
from broker import ChoreographyEventBroker

class OrderMicroservice:
    def __init__(self, broker: ChoreographyEventBroker) -> None:
        self.broker = broker
        self.db: Dict[str, Any] = {}
        self.outbox: List[Dict[str, Any]] = []

    async def create_new_order(self, correlation_id: Any, total_cost: float, simulate_failure: bool) -> None:
        # Atomic Write Block simulation: Database and Outbox updated as one unit
        order_id = f"ORD_{correlation_id.hex[:6].upper()}"
        self.db[order_id] = {"status": "SUBMITTED", "cost": total_cost}
        
        evt = ChoreographyEvent(
            correlation_id=correlation_id,
            event_type="ORDER_SUBMITTED",
            sender="ORDER_SERVICE",
            payload={"order_id": order_id, "cost": total_cost, "force_fail": simulate_failure}
        )
        self.outbox.append({"processed": False, "event": evt})
        print(f"[ORDER SERVICE] [OUTBOX COMMITTED] State saved for {order_id}. Outbox staged.")
        
        await self.flush_outbox()

    async def flush_outbox(self) -> None:
        for record in self.outbox:
            if not record["processed"]:
                record["processed"] = True
                await self.broker.broadcast(record["event"])

    async def compensate_order(self, event: ChoreographyEvent) -> None:
        target_order = event.payload.get("order_id")
        for oid in self.db:
            if oid == target_order:
                self.db[oid]["status"] = "CANCELLED_CHOREOGRAPHY"
                print(f"[ORDER SERVICE] [CHOREOGRAPHY ROLLBACK] Restored stability -> Order {oid} marked CANCELLED.")


class InventoryMicroservice:
    def __init__(self, broker: ChoreographyEventBroker) -> None:
        self.broker = broker
        self.db: Dict[str, Any] = {}
        self.processed_ids: Set[Any] = set()

    async def handle_order_submitted(self, event: ChoreographyEvent) -> None:
        # Idempotency Filter check
        if event.event_id in self.processed_ids:
            return
        
        print(f"       <- [INVENTORY SERVICE] Processing event request ID: {event.event_id}")
        self.processed_ids.add(event.event_id)
        
        order_id = event.payload.get("order_id")
        # Commit local stock allocation directly to DB
        self.db[order_id] = "STOCK_HOLD_CONFIRMED"
        print(f"[INVENTORY SERVICE] Stock held cleanly for {order_id}.")

        # Advance workflow autonomously by emitting next domain step event
        next_evt = ChoreographyEvent(
            correlation_id=event.correlation_id,
            event_type="STOCK_ALLOCATED",
            sender="INVENTORY_SERVICE",
            payload=event.payload
        )
        await self.broker.broadcast(next_evt)

    async def handle_billing_failed(self, event: ChoreographyEvent) -> None:
        order_id = event.payload.get("order_id")
        if order_id in self.db:
            self.db[order_id] = "STOCK_RELEASED_COMPENSATION"
            print(f"[INVENTORY SERVICE] [CHOREOGRAPHY ROLLBACK] Restored stability -> Stock dropped for {order_id}.")


class FinancialBillingMicroservice:
    def __init__(self, broker: ChoreographyEventBroker) -> None:
        self.broker = broker
        self.processed_ids: Set[Any] = set()

    async def handle_stock_allocated(self, event: ChoreographyEvent) -> None:
        if event.event_id in self.processed_ids:
            return
        self.processed_ids.add(event.event_id)
        
        print(f"       <- [BILLING SERVICE] Processing event request ID: {event.event_id}")
        order_id = event.payload.get("order_id")
        
        if event.payload.get("force_fail", False):
            print(f"[BILLING SERVICE] ❌ TRANSACTION REJECTED for {order_id}.")
            fail_evt = ChoreographyEvent(
                correlation_id=event.correlation_id,
                event_type="BILLING_FAILED",
                sender="BILLING_SERVICE",
                payload={"order_id": order_id}
            )
            await self.broker.broadcast(fail_evt)
        else:
            print(f"[BILLING SERVICE] ✓ Charge captured successfully for {order_id}.")