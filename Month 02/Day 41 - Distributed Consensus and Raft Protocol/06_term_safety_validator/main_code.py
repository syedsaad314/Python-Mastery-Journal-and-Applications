"""
Core Topic: Term-Based Safety Validations
Description: Drops incoming RPC payloads if they contain stale terms, preserving leadership safety.
Lead Engineer: Syed Saad Bin Irfan
"""

class TermSafetyValidator:
    """Protects a node from executing commands sent by isolated or historical leaders."""
    
    def __init__(self, native_term: int) -> None:
        self.native_term = native_term

    def validate_incoming_rpc_term(self, remote_term: int) -> bool:
        """Evaluates term numbers, dropping the request if the remote sender's term is stale."""
        if remote_term < self.native_term:
            print(f"[SAFETY-REJECT] Dropping RPC. Remote term ({remote_term}) is older than current term ({self.native_term}).")
            return False
            
        print(f"[SAFETY-ACCEPT] RPC term validation passed. Remote Term: {remote_term}")
        return True


if __name__ == "__main__":
    validator = TermSafetyValidator(native_term=4)
    
    # Simulate a network-isolated leader rejoining the cluster with an outdated term
    validator.validate_incoming_rpc_term(remote_term=3)
    # Simulate a valid message from a contemporary or advanced term
    validator.validate_incoming_rpc_term(remote_term=4)