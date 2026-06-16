"""
Core Topic: Asynchronous Backward Compensation Loops
Description: Executes inverted compensating actions to roll back partial writes in reverse order.
Lead Engineer: Syed Saad Bin Irfan
"""

from typing import List, Dict

class CompensatingTransactionEngine:
    """Tracks completed steps and executes compensating actions in reverse order on failure."""
    
    def __init__(self) -> None:
        self.executed_history: List[str] = []
        # Inverted mapping dictionary for compensations
        self.compensation_registry: Dict[str, str] = {
            "CHARGE_CREDIT_CARD": "REFUND_CREDIT_CARD",
            "HOLD_WAREHOUSE_STOCK": "RELEASE_WAREHOUSE_STOCK",
            "GENERATE_INVOICE": "VOID_INVOICE"
        }

    def register_execution_success(self, step_name: str) -> None:
        self.executed_history.append(step_name)

    def execute_backward_compensation_loop(self) -> List[str]:
        """Triggers compensating routines in reverse order (LIFO) to ensure clean rollbacks."""
        rollback_actions_triggered = []
        
        # Reverse processing order to preserve consistency invariants
        for step in reversed(self.executed_history):
            compensating_action = self.compensation_registry.get(step, "NO_COMPREHENSIVE_ACTION_FOUND")
            rollback_actions_triggered.append(compensating_action)
            
        self.executed_history.clear()
        return rollback_actions_triggered


if __name__ == "__main__":
    engine = CompensatingTransactionEngine()
    
    # Simulate a partial success path before hitting a downstream crash
    engine.register_execution_success("CHARGE_CREDIT_CARD")
    engine.register_execution_success("HOLD_WAREHOUSE_STOCK")
    
    print(f"[COMPENSATION-ENGINE] Forward execution history tracked: {engine.executed_history}")
    reversal_sequence = engine.execute_backward_compensation_loop()
    print(f"[COMPENSATION-ENGINE] Reversal sequence executed: {reversal_sequence}")