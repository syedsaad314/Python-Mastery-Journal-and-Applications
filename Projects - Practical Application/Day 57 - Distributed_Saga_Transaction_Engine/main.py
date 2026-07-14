# Lead Engineer: Syed Saad Bin Irfan
"""
Portfolio Layer: Master Verification Harness for the Saga Engine
"""
import asyncio
from models import SagaStepDefinition
from services import OrderProcessingService, WarehouseInventoryService, BillingLedgerService
from orchestrator import DistributedSagaOrchestrator

async def run_system_verification() -> None:
    print("=========================================================================")
    print("        RUNNING ACTIVATION TRACK: DISTRIBUTED ORCHESTRATION SAGA         ")
    print("=========================================================================")

    # Wire up the step configurations
    saga_pipeline = [
        SagaStepDefinition(
            name="Order Booking", 
            action_coro=OrderProcessingService.book_order, 
            compensate_coro=OrderProcessingService.cancel_order
        ),
        SagaStepDefinition(
            name="Inventory Reservation", 
            action_coro=WarehouseInventoryService.assign_stock, 
            compensate_coro=WarehouseInventoryService.free_stock
        ),
        SagaStepDefinition(
            name="Ledger Billing Capture", 
            action_coro=BillingLedgerService.charge_account, 
            compensate_coro=BillingLedgerService.credit_account
        )
    ]
    
    orchestrator = DistributedSagaOrchestrator(step_pipeline=saga_pipeline)

    # -------------------------------------------------------------------------
    # SCENARIO 1: The Happy Path Sequence
    # -------------------------------------------------------------------------
    print("\n=== SCENARIO 1: Verifying Successful Forward Path ===")
    happy_payload = {"user_token_id": "usr_alpha", "purchase_cost": 89.50, "force_credit_rejection": False}
    happy_result_context = await orchestrator.launch_orchestration_flow(happy_payload)
    
    print("\n[VERIFICATION RESULTS - SCENARIO 1]")
    print(f"Final Saga Status Check: {happy_result_context.status.value}")
    print(f"Final Microservices State Map: {happy_result_context.results}")

    # -------------------------------------------------------------------------
    # SCENARIO 2: Downstream Failure & Automatic Balancing Rollback
    # -------------------------------------------------------------------------
    print("\n=== SCENARIO 2: Verifying Downstream Error & Compensation Path ===")
    failure_payload = {"user_token_id": "usr_beta", "purchase_cost": 9999.00, "force_credit_rejection": True}
    failure_result_context = await orchestrator.launch_orchestration_flow(failure_payload)
    
    print("\n[VERIFICATION RESULTS - SCENARIO 2]")
    print(f"Final Saga Status Check: {failure_result_context.status.value}")
    print(f"Final Microservices State Map: {failure_result_context.results}")
    print(f"Captured System Errors: {failure_result_context.errors}")

if __name__ == "__main__":
    asyncio.run(run_system_verification())