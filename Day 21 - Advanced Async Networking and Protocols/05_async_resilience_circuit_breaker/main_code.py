"""
Core Topic: Asynchronous Circuit Breaker Pattern
Description: Wraps network logic in a resilient state machine to prevent cascading system failures.
Lead Engineer: Syed Saad Bin Irfan
"""

import asyncio
import time

class AsyncCircuitBreakerException(Exception): pass

class AsyncCircuitBreaker:
    def __init__(self, failure_ceiling: int = 2, recovery_timeout_sec: float = 1.0) -> None:
        self.failure_threshold: int = failure_ceiling
        self.recovery_timeout: float = recovery_timeout_sec
        self.state: str = "CLOSED"  # CLOSED, OPEN, HALF-OPEN
        self.failure_counter: int = 0
        self.last_state_change_time: float = time.time()

    async def execute(self, target_coroutine) -> any:
        """Executes an async task while checking and maintaining the internal circuit state."""
        current_time = time.time()
        
        # Check if an OPEN circuit has completed its timeout window to enter HALF-OPEN state
        if self.state == "OPEN":
            if current_time - self.last_state_change_time > self.recovery_timeout:
                self.state = "HALF-OPEN"
                print("[CIRCUIT] Timeout complete. Switching state to HALF-OPEN...")
            else:
                raise AsyncCircuitBreakerException("Circuit state is OPEN. Request rejected defensively.")

        try:
            result = await target_coroutine
            # If a HALF-OPEN request succeeds, close the circuit and reset metrics
            if self.state == "HALF-OPEN":
                self.state = "CLOSED"
                self.failure_counter = 0
                print("[CIRCUIT] Transaction succeeded in HALF-OPEN. Resetting circuit to CLOSED.")
            return result
        except Exception as operation_error:
            self.failure_counter += 1
            print(f"[CIRCUIT] Caught operation fault. Failure count: {self.failure_counter}")
            
            # Trip the circuit to OPEN if failures exceed the threshold
            if self.failure_counter >= self.failure_threshold:
                self.state = "OPEN"
                self.last_state_change_time = time.time()
                print("[CIRCUIT] Error threshold breached. Tripping circuit state to OPEN.")
            raise operation_error

async def mock_network_dependency(should_fail: bool) -> str:
    await asyncio.sleep(0.05)
    if should_fail:
        raise ConnectionRefusedError("Remote interface unreachable.")
    return "API_TRANSACTION_SUCCESS"

async def main() -> None:
    breaker = AsyncCircuitBreaker(failure_ceiling=2, recovery_timeout_sec=0.2)

    # Trigger initial failures to test circuit trip mechanisms
    for _ in range(2):
        try:
            await breaker.execute(mock_network_dependency(should_fail=True))
        except ConnectionRefusedError:
            pass

    # Verify that the circuit blocks subsequent calls defensively
    try:
        await breaker.execute(mock_network_dependency(should_fail=False))
    except AsyncCircuitBreakerException as e:
        print(f"[MAIN] Defended call captured: {e}")

if __name__ == "__main__":
    asyncio.run(main())