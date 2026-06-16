"""
Core Topic: Distributed Idempotency Validation
Description: Guarantees that duplicate incoming network events are executed exactly once.
Lead Engineer: Syed Saad Bin Irfan
"""

from typing import Dict, Any

class IdempotencyKeyValidator:
    """Checks and catches duplicate incoming requests to prevent double-processing data writes."""
    
    def __init__(self) -> None:
        self.processed_requests_vault: Dict[str, Any] = {}

    def execute_safely(self, idempotency_key: str, payload_action: callable, *args, **kwargs) -> Any:
        """Executes a business action only if the accompanying idempotency key is unique."""
        if idempotency_key in self.processed_requests_vault:
            print(f"[IDEMPOTENCY-ALERTER] Key '{idempotency_key}' already seen! Returning cached execution output.")
            return self.processed_requests_vault[idempotency_key]

        # Execute the operation if the key is new
        execution_output = payload_action(*args, **kwargs)
        self.processed_requests_vault[idempotency_key] = execution_output
        return execution_output


if __name__ == "__main__":
    validator = IdempotencyKeyValidator()
    
    def deduct_funds(account: str, value: float) -> str:
        return f"Deducted {value} from {account} successfully."

    # First delivery processing loop
    res_1 = validator.execute_safely("req-id-5512", deduct_funds, account="saad-khi", value=1500.0)
    print(f"[IDEMPOTENCY-RUN-1] Result: {res_1}")

    # Second duplicate retry event delivery
    res_2 = validator.execute_safely("req-id-5512", deduct_funds, account="saad-khi", value=1500.0)
    print(f"[IDEMPOTENCY-RUN-2] Result: {res_2}")