# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Asynchronous Forward Execution Workflow Loop
Description: Implements sequential task execution logic that advances a transaction 
             step-by-step through independent local microservices.
"""
import asyncio
from typing import List, Dict, Any, Callable, Coroutine

class ForwardWorkflowEngine:
    def __init__(self) -> None:
        self.history: List[str] = []

    async def execute_chain(self, context: Dict[str, Any], steps: List[Callable[[Dict[str, Any]], Coroutine[Any, Any, None]]]) -> bool:
        for step in steps:
            step_name = step.__name__
            try:
                await step(context)
                self.history.append(step_name)
            except Exception as e:
                print(f"[EXECUTION FAILURE] Break at step '{step_name}': {e}")
                return False
        return True

# Mock steps for local isolation testing
async def reserve_credit(ctx: Dict[str, Any]) -> None:
    ctx["credit_reserved"] = True

async def hold_inventory(ctx: Dict[str, Any]) -> None:
    # Simulating an unexpected downstream application failure
    raise RuntimeError("Inventory capacity exceeded")

if __name__ == "__main__":
    shared_context = {"order_id": "9921"}
    engine = ForwardWorkflowEngine()
    
    success = asyncio.run(engine.execute_chain(shared_context, [reserve_credit, hold_inventory]))
    assert success is False
    assert engine.history == ["reserve_credit"]