"""
Core Topic: Monotonic Term Number Validation
Description: Guarantees term numbers increase monotonically and handles old leaders.
Lead Engineer: Syed Saad Bin Irfan
"""

class MonotonicTermValidator:
    """Tracks and validates term counters to ensure safety across the cluster."""
    
    def __init__(self, node_id: str, initial_term: int = 0) -> None:
        self.node_id = node_id
        self.current_term = initial_term
        self.is_leader = False

    def examine_incoming_term(self, incoming_term: int) -> bool:
        """Evaluates an incoming term counter against the local node's current term."""
        if incoming_term > self.current_term:
            self.current_term = incoming_term
            if self.is_leader:
                print(f"[TERM-VALIDATOR] Node '{self.node_id}' discovered higher term ({incoming_term}). Stepping down.")
                self.is_leader = False
            return True
        return False


if __name__ == "__main__":
    # Simulate an isolated leader from an older network partition returning to the cluster
    stale_leader = MonotonicTermValidator("node-old-leader", initial_term=1)
    stale_leader.is_leader = True
    
    # An incoming heartbeat arrives from the new cluster leader with a higher term counter
    stale_leader.examine_incoming_term(incoming_term=2)
    print(f" -> Post-evaluation status: Active Leader Role = {stale_leader.is_leader} | Term = {stale_leader.current_term}")