"""
Core Topic: Generator Coroutine Suspension Mechanics
Description: Uses raw generator yields as explicit cooperative context-switching boundaries.
Lead Engineer: Syed Saad Bin Irfan
"""

from typing import Generator, Tuple, Any

# Types defining the yield format: Tuple[Event_Type: str, Target_Socket_Descriptor: Any]
CoroutineYieldSignature = Generator[Tuple[str, Any], Any, None]

class CooperativeTaskRoutine:
    """Simulates an asynchronous workload routine using generator-driven yield states."""
    
    def __init__(self, task_id: int, target_mock_fd: int) -> None:
        self.task_id: int = task_id
        self.fd: int = target_mock_fd

    def execute_sequence(self) -> CoroutineYieldSignature:
        """Executes sequential task steps, yielding control back to the engine during I/O blocks."""
        print(f"[COROUTINE-{self.task_id}] Executing initial compute phase...")
        
        # Yield control back to the scheduler line to wait for read readiness
        yield ("read", self.fd)
        
        print(f"[COROUTINE-{self.task_id}] Execution resumed post-read notification. Packing response payload...")
        
        # Yield control again to wait for write availability
        yield ("write", self.fd)
        
        print(f"[COROUTINE-{self.task_id}] Pipeline completed safely.")


if __name__ == "__main__":
    routine = CooperativeTaskRoutine(task_id=101, target_mock_fd=12)
    generator_inst = routine.execute_sequence()
    
    # Drive the generator manually to observe the context switching milestones
    state_one = generator_inst.send(None)
    print(f"[DRIVER] Intercepted Task suspension point: {state_one}")
    
    state_two = generator_inst.send(None)
    print(f"[DRIVER] Intercepted Task suspension point: {state_two}")
    
    try:
        generator_inst.send(None)
    except StopIteration:
        print("[DRIVER] Coroutine generator exited naturally.")