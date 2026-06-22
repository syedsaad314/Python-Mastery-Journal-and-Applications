"""
Core Topic: Forward Recovery Retry Mechanics
Description: Implements exponential backoff retries for transient failures before choosing rollback options.
Lead Engineer: Syed Saad Bin Irfan
"""

import time
from typing import Callable, Any

class ForwardRecoveryRetryEngine:
    """Applies execution retry loops with time backoffs to handle transient network hiccups safely."""
    
    @staticmethod
    def invoke_with_exponential_backoff(action: Callable, max_attempts: int, initial_delay: float) -> Any:
        delay = initial_delay
        
        for attempt in range(1, max_attempts + 1):
            try:
                return action()
            except Exception as error:
                print(f"[RETRY-ENGINE] Attempt {attempt} failed with error: {error}. Retrying in {delay}s...")
                if attempt == max_attempts:
                    raise RuntimeError("MAX_RETRIES_EXCEEDED_SWITCH_TO_COMPENSATION")
                time.sleep(delay)
                delay *= 2 # Exponentially scale the time delay increment


if __name__ == "__main__":
    attempt_counter = 0
    
    def unstable_network_rpc() -> str:
        global attempt_counter
        attempt_counter += 1
        if attempt_counter < 3:
            raise ConnectionError("Timeout error connecting to regional shard endpoint.")
        return "RPC_CONNECTION_SUCCESSFUL"

    print("[FORWARD-RECOVERY] Launching transaction step with exponential backoff guards...")
    final_output = ForwardRecoveryRetryEngine.invoke_with_exponential_backoff(
        action=unstable_network_rpc, max_attempts=4, initial_delay=0.1
    )
    print(f"[FORWARD-RECOVERY] Operation recovered successfully. Output payload: {final_output}")