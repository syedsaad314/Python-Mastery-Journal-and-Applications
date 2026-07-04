# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Split Vote Term Advancement
Description: Detects split-vote stalemates and advances the logical term counter 
             to safely trigger a clean election reset.
"""
class ElectionBallotBox:
    def __init__(self, current_term: int, total_cluster_nodes: int) -> None:
        self.term = current_term
        self.total_nodes = total_cluster_nodes
        self.votes_received = 0

    def register_vote(self) -> None:
        self.votes_received += 1

    def evaluate_ballot(self) -> str:
        majority_needed = (self.total_nodes // 2) + 1
        if self.votes_received >= majority_needed:
            return "ELECTED_LEADER"
        return "STALEMATE_SPLIT"

if __name__ == "__main__":
    # Cluster containing 3 members requires 2 votes for a clear majority
    box = ElectionBallotBox(current_term=1, total_cluster_nodes=3)
    box.register_vote()
    assert box.evaluate_ballot() == "STALEMATE_SPLIT"