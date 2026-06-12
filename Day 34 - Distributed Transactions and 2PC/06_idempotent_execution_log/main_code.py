"""
Core Topic: Idempotent Transaction Execution Log
Description: Filters out duplicate incoming transaction requests using deduplication tokens.
Lead Engineer: Syed Saad Bin Irfan
"""

from typing import Set

class IdempotentTransactionGateway:
    """Filters incoming transactions to guarantee requests are processed exactly once."""
    
    def __init__(self) -> None:
        # Set of tracked unique transaction IDs
        self.processed_transaction_ids: Set[str] = set()

    def process_transaction(self, tx_id: str, command: str) -> str:
        """Processes the transaction only if its unique ID has not been seen before."""
        if tx_id in self.processed_transaction_ids:
            return "REJECTED_DUPLICATE_IDEMPOTENT_TRIGGER"
            
        self.processed_transaction_ids.add(tx_id)
        return f"SUCCESS_PROCESSED_COMMAND:{command}"


if __name__ == "__main__":
    gateway = IdempotentTransactionGateway()
    
    # Simulate a client sending a transaction request
    res_1 = gateway.process_transaction("TX-UUID-77A1", "Deduct-1000-PKR")
    # Simulate a network retry sending the exact same transaction request again
    res_2 = gateway.process_transaction("TX-UUID-77A1", "Deduct-1000-PKR")
    
    print(f"[IDEMPOTENCY-GATEWAY] First execution response: {res_1}")
    print(f"[IDEMPOTENCY-GATEWAY] Network retry execution response: {res_2}")