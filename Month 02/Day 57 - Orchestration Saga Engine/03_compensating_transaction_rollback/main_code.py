# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Automated Reverse Compensating Transaction Rollback
Description: Steps backward through the recorded execution history to trigger 
             compensating actions that revert system state on failure.
"""
import asyncio
from typing import List, Dict, Any, Callable, Coroutine

class CompensationRollbackEngine:
    def __init__(self) -> None:
        self.rollback_log: List[str] = []

    async def trigger_reverse_rollback(
        self, 
        history: List[str], 
        compensations: Dict[str, Callable[[Dict[str, Any]], Coroutine[Any, Any, None]]],
        context: Dict[str, Any]
    ) -> None:
        # Step backward through the execution stack to undo changes in reverse order
        for step_name in reversed(history):
            if step_name in compensations:
                await compensations[step_name](context)
                self.rollback_log.append(f"COMPENSATE_SUCCESS:{step_name}")

# Mock compensation targets
async def undo_credit(ctx: Dict[str, Any]) -> None:
    ctx["credit_reserved"] = False

if __name__ == "__main__":
    mock_history = ["reserve_credit"]
    mock_compensations = {"reserve_credit": undo_credit}
    state_ctx = {"credit_reserved": True}
    
    engine = CompensationRollbackEngine()
    asyncio.run(engine.trigger_reverse_rollback(mock_history, mock_compensations, state_ctx))
    
    assert state_ctx["credit_reserved"] is False
    assert engine.rollback_log[0] == "COMPENSATE_SUCCESS:reserve_credit"