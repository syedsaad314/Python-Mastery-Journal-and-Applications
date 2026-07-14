# Lead Engineer: Syed Saad Bin Irfan
"""
Portfolio Layer: Decoupled Independent Microservices Implementing Compensations
"""
import asyncio
from models import SagaContext

class OrderProcessingService:
    @staticmethod
    async def book_order(ctx: SagaContext) -> None:
        print("[ORDER SERVICE] Booking pending order entry...")
        await asyncio.sleep(0.01)
        ctx.results["order_id"] = "ORD_7071"
        ctx.results["order_state"] = "PENDING_RESERVATION"

    @staticmethod
    async def cancel_order(ctx: SagaContext) -> None:
        print("[ORDER SERVICE] Rollback compensation: Evicting unverified order reservation...")
        await asyncio.sleep(0.01)
        ctx.results["order_state"] = "EVICTED_ROLLBACK"

class WarehouseInventoryService:
    @staticmethod
    async def assign_stock(ctx: SagaContext) -> None:
        print("[INVENTORY SERVICE] Securing item reservation allocations...")
        await asyncio.sleep(0.01)
        ctx.results["inventory_allocated"] = True

    @staticmethod
    async def free_stock(ctx: SagaContext) -> None:
        print("[INVENTORY SERVICE] Rollback compensation: Releasing warehouse items back to stock pool...")
        await asyncio.sleep(0.01)
        ctx.results["inventory_allocated"] = False

class BillingLedgerService:
    @staticmethod
    async def charge_account(ctx: SagaContext) -> None:
        print("[BILLING SERVICE] Authorizing settlement transaction against card balance...")
        await asyncio.sleep(0.01)
        if ctx.payload.get("force_credit_rejection", False):
            raise RuntimeError("CRITICAL: Overdraft limits exceeded — Transaction Authorization Denied.")
        ctx.results["billing_captured"] = True

    @staticmethod
    async def credit_account(ctx: SagaContext) -> None:
        print("[BILLING SERVICE] Rollback compensation: Refunding payment back to account balance...")
        await asyncio.sleep(0.01)
        ctx.results["billing_captured"] = False