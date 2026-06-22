"""
Core Topic: Raft Term Epoch Tracking
Description: Validates incoming messages by checking term numbers to drop out-of-date entries.
Lead Engineer: Syed Saad Bin Irfan
"""

class TermEpochValidator:
    def __init__(self, current_term: int) -> None:
        self.current_term = current_term

    def validate_incoming_term(self, remote_term: int) -> bool:
        """Rejects requests from out-of-date terms, or updates local term if a newer term is seen."""
        if remote_term < self.current_term:
            print(f"[TERM-REJECT] Stale term detected ({remote_term} < {self.current_term}). Dropping request.")
            return False
            
        if remote_term > self.current_term:
            print(f"[TERM-UPDATE] Stepping down. Updating local term from {self.current_term} to {remote_term}.")
            self.current_term = remote_term
            
        return True


if __name__ == "__main__":
    validator = TermEpochValidator(current_term=3)
    # Stale terms from delayed network messages must be dropped instantly
    assert validator.validate_incoming_term(remote_term=2) == False
    # Newer terms force the current node to update its tracking state and step down if needed
    assert validator.validate_incoming_term(remote_term=4) == True
    assert validator.current_term == 4