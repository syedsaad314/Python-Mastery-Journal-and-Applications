"""
System: Multi-Service Orchestrated Saga E-Commerce Engine
Description: Emulates an asynchronous enterprise Saga transaction pipeline. Coordinates Order,
             Payment, and Inventory service calls sequentially without distributed locks, 
             using clean compensation workflows to roll back changes automatically if errors occur.
Lead Engineer: Syed Saad Bin Irfan
"""

import logging
import uuid
from typing import Dict, List, Any

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)s] (SagaOrchestrator) %(message)s')

class MicroserviceShard:
    """A decentralized microservice shard running isolated local transaction operations."""
    
    def __init__(self, name: str) -> None:
        self.name = name
        self.ledger: Dict[str, str] = {}

    def execute_forward_action(self, tx_id: str, detail: str) -> bool:
        """Executes a local forward transaction write."""
        if "FAIL_TRIGGER" in detail:
            logging.warning(f"[{self.name}] Error processed during forward execution for context: {detail}")
            return False
        self.ledger[tx_id] = f"COMMITTED_DATA_{detail}"
        logging.info(f"[{self.name}] Step Successful for transaction {tx_id}. Ledger Saved.")
        return True

    def execute_compensating_action(self, tx_id: str) -> None:
        """Reverses a previously committed local transaction to restore consistency."""
        if tx_id in self.ledger:
            del self.ledger[tx_id]
            logging.warning(f"[{self.name}] Compensation Triggered for transaction {tx_id}. Local write reverted cleanly.")


class ECommerceSagaOrchestratorEngine:
    """Orchestrates sequential service tasks, managing compensations if any step fails."""
    
    def __init__(self, services: Dict[str, MicroserviceShard]) -> None:
        self.services = services

    def process_distributed_transaction(self, order_id: str, action_manifest: List[Dict[str, Any]]) -> bool:
        logging.info(f"======================================================================")
        logging.info(f"[SAGA-ENGINE] Initializing Saga Transaction Workflow Path for ID: {order_id}")
        logging.info(f"======================================================================")
        
        successful_steps_history: List[str] = []
        saga_failed = False

        # PHASE 1: Sequential Forward Execution Track
        for step in action_manifest:
            service_name = step["service"]
            action_detail = step["detail"]
            target_service = self.services[service_name]

            # Execute the local transaction on the target service
            success = target_service.execute_forward_action(order_id, action_detail)
            
            if success:
                successful_steps_history.append(service_name)
            else:
                logging.error(f"[SAGA-ENGINE] Critical failure hit at service step: '{service_name}'")
                saga_failed = True
                break

        # PHASE 2: Asynchronous Backward Compensation Track (Triggered only on failure)
        if saga_failed:
            logging.warning(f"[SAGA-ENGINE] Initiating backward rollback compensation loop...")
            for completed_service in reversed(successful_steps_history):
                self.services[completed_service].execute_compensating_action(order_id)
            logging.info("[SAGA-ENGINE] Eventual Consistency restored successfully via full rollback.")
            return False

        logging.info("[SAGA-ENGINE] Distributed Saga Transaction finished successfully. Data is consistent.")
        return True


if __name__ == "__main__":
    # Initialize decoupled business microservice shards
    payment_shard   = MicroserviceShard("PaymentService")
    inventory_shard = MicroserviceShard("InventoryService")
    shipping_shard  = MicroserviceShard("ShippingService")
    
    cluster_services = {
        "PaymentService": payment_shard,
        "InventoryService": inventory_shard,
        "ShippingService": shipping_shard
    }
    
    orchestrator = ECommerceSagaOrchestratorEngine(cluster_services)

    # Scenario A: A standard transaction where all services complete successfully
    tx_id_a = str(uuid.uuid4())[:8]
    manifest_a = [
        {"service": "PaymentService", "detail": "CREDIT_CHARGE_USD_500"},
        {"service": "InventoryService", "detail": "ALLOCATE_ITEM_QUANTITY_1"},
        {"service": "ShippingService", "detail": "GENERATE_TRACKING_LABEL"}
    ]
    orchestrator.process_distributed_transaction(tx_id_a, manifest_a)

    print("\n----------------------------------------------------------------------\n")

    # Scenario B: A transaction that fails at the final shipping step, triggering a complete compensation rollback
    tx_id_b = str(uuid.uuid4())[:8]
    manifest_b = [
        {"service": "PaymentService", "detail": "CREDIT_CHARGE_USD_120"},
        {"service": "InventoryService", "detail": "ALLOCATE_ITEM_QUANTITY_4"},
        {"service": "ShippingService", "detail": "FAIL_TRIGGER_OUT_OF_BOUNDS"} # Shipping failure
    ]
    orchestrator.process_distributed_transaction(tx_id_b, manifest_b)