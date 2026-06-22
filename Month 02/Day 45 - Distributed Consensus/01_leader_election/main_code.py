"""
Core Topic: Raft Leader Election State Transitions
Description: Models node state transitions between Follower, Candidate, and Leader based on votes.
Lead Engineer: Syed Saad Bin Irfan
"""

class ConsensusNodeRole:
    def __init__(self, node_id: str) -> None:
        self.node_id = node_id
        self.current_role = "Follower"
        self.votes_received = 0

    def trigger_election_timeout(self) -> None:
        """Transitions node to candidate status and self-votes when an election timeout fires."""
        self.current_role = "Candidate"
        self.votes_received = 1
        print(f"[ELECTION] Node {self.node_id} timed out. Transitioned to Candidate. Self-vote cast.")

    def evaluate_vote_count(self, total_cluster_nodes: int) -> bool:
        """Promotes node to Leader if a strict majority quorum is met."""
        majority_needed = (total_cluster_nodes // 2) + 1
        if self.current_role == "Candidate" and self.votes_received >= majority_needed:
            self.current_role = "Leader"
            print(f"[ELECTION-WIN] Node {self.node_id} received {self.votes_received} votes. Promoted to Leader.")
            return True
        return False


if __name__ == "__main__":
    node = ConsensusNodeRole("node-01")
    node.trigger_election_timeout()
    node.votes_received += 2 # Accumulate peer network votes
    assert node.evaluate_vote_count(total_cluster_nodes=5) == True
    assert node.current_role == "Leader"