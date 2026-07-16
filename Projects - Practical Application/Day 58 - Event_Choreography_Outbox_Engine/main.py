# Lead Engineer: Syed Saad Bin Irfan
"""
Portfolio Layer: Master Operational Verification Harness for Choreography Engine
"""
import asyncio
import uuid
from broker import ChoreographyEventBroker
from services import OrderMicroservice, InventoryMicroservice, FinancialBillingMicroservice

async def execution_harness() -> None:
    print("=========================================================================")
    print("      RUNNING ACTIVATION TRACK: DECOUPLED CHOREOGRAPHY SAGA ENGINE      ")
    print("=========================================================================")

    # Initialize the centralized messaging bus hub infrastructure
    message_bus = ChoreographyEventBroker()

    # Wire up the participating services
    order_svc = OrderMicroservice(message_bus)
    inventory_svc = InventoryMicroservice(message_bus)
    billing_svc = FinancialBillingMicroservice(message_bus)

    # Register event subscriptions across the cluster to establish the choreography paths
    message_bus.subscribe("ORDER_SUBMITTED", inventory_svc.handle_order_submitted)
    message_bus.subscribe("STOCK_ALLOCATED", billing_svc.handle_stock_allocated)
    message_bus.subscribe("BILLING_FAILED", order_svc.compensate_order)
    message_bus.subscribe("BILLING_FAILED", inventory_svc.handle_billing_failed)

    # -------------------------------------------------------------------------
    # SCENARIO 1: The Completely Successful Asynchronous Flow
    # -------------------------------------------------------------------------
    print("\n--- SCENARIO 1: Verifying Autonomous Happy Path Track ---")
    tx_token_1 = uuid.uuid4()
    await order_svc.create_new_order(correlation_id=tx_token_1, total_cost=299.00, simulate_failure=False)
    
    await asyncio.sleep(0.05) # Give async processing loops a brief window to complete
    print("\n[DB SNAPSHOT - SCENARIO 1]")
    print(f"Order Service Database State Matrix: {order_svc.db}")
    print(f"Inventory Service Database State Matrix: {inventory_svc.db}")

    # -------------------------------------------------------------------------
    # SCENARIO 2: Downstream Error Triggering Automatic Compensations
    # -------------------------------------------------------------------------
    print("\n--- SCENARIO 2: Verifying Failure Signal & Decentralized Rollback Track ---")
    tx_token_2 = uuid.uuid4()
    await order_svc.create_new_order(correlation_id=tx_token_2, total_cost=9999.00, simulate_failure=True)
    
    await asyncio.sleep(0.05) # Allow async events to propagate completely
    print("\n[DB SNAPSHOT - SCENARIO 2]")
    print(f"Order Service Database State Matrix: {order_svc.db}")
    print(f"Inventory Service Database State Matrix: {inventory_svc.db}")

if __name__ == "__main__":
    asyncio.run(execution_harness())