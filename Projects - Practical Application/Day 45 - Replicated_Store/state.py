"""
Component: Node Consensus State Tracking
Description: Encapsulates node consensus status, terms, roles, and voted-for metrics.
Lead Engineer: Syed Saad Bin Irfan
"""

class NodeConsensusState:
    """Manages a node's local consensus state, role tracking, and term configurations."""
    
    def __init__(self, node_id: str) -> None:
        self.node_id = node_id
        self.current_term = 0
        self.current_role = "Follower"  # Options: Follower, Candidate, Leader
        self.voted_for = None
        self.commit_index = -1

    def transition_to_follower(self, term: int) -> None:
        self.current_role = "Follower"
        self.current_term = term
        self.voted_for = None

    def transition_to_candidate(self) -> None:
        self.current_role = "Candidate"
        self.current_term += 1
        self.voted_for = self.node_id  # Automatically vote for self

    def transition_to_leader(self) -> None:
        self.current_role = "Leader"
        self.voted_for = None