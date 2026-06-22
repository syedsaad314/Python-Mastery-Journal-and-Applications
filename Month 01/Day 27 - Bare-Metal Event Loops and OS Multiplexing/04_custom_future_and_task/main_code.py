"""
Core Topic: Custom Future and Task Resolution Architectures
Description: Bridges state notifications with execution blocks through custom Task tracking classes.
Lead Engineer: Syed Saad Bin Irfan
"""

from typing import Callable, List, Any, Optional

class CustomFuture:
    """Tracks a pending asynchronous computation result along with its completion triggers."""
    
    def __init__(self) -> None:
        self._result: Any = None
        self._is_resolved: bool = False
        self._callbacks: List[Callable[["CustomFuture"], None]] = []

    def set_result(self, completion_value: Any) -> None:
        if self._is_resolved:
            raise RuntimeError("Cannot re-resolve an active future construct.")
        self._result = completion_value
        self._is_resolved = True
        # Fire all registered event callbacks immediately
        for callback in self._callbacks:
            callback(self)

    def add_done_callback(self, callback: Callable[["CustomFuture"], None]) -> None:
        if self._is_resolved:
            callback(self)
        else:
            self._callbacks.append(callback)


class TrackedExecutionTask:
    """Drives generator lifecycles automatically using event-driven future resolutions."""
    
    def __init__(self, generator_coro: Any) -> None:
        self.coro = generator_coro
        self.step_execution()

    def step_execution(self, completed_future: Optional[CustomFuture] = None) -> None:
        """Advances the wrapped coroutine loop whenever a pending future resolves."""
        try:
            send_payload = completed_future._result if completed_future else None
            next_yielded_node = self.coro.send(send_payload)
            
            # If the coroutine yields a future object, bind execution advancement to its resolution
            if isinstance(next_yielded_node, CustomFuture):
                next_yielded_node.add_done_callback(self.step_execution)
        except StopIteration:
            # Coroutine completed execution lifecycle runs safely
            pass


# --- Demonstration Coroutine Hook ---
def sample_task_runner(future_handle: CustomFuture):
    print("[TASK] Running initial processing steps. Waiting on future resolution token...")
    resolved_string = yield future_handle
    print(f"[TASK] Execution resumed! Captured resolution payload value: {resolved_string}")

if __name__ == "__main__":
    fut = CustomFuture()
    coro_instance = sample_task_runner(fut)
    
    # Initialize the tracking engine wrapper to kick off step execution
    task_wrapper = TrackedExecutionTask(coro_instance)
    
    print("[MAIN] Simulating external event completion events...")
    fut.set_result("UBIT_CLUSTER_READY_TOKEN")