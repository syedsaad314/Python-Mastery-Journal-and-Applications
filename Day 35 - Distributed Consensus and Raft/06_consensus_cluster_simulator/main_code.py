"""
Core Topic: Consensus Cluster Simulator Loop
Description: Demonstrates an election loop calculating simple quorum majorities.
Lead Engineer: Syed Saad Bin Irfan
"""

from typing import List, Dict

class SimpleConsensusNode:
    def __init__(self, node_id: str) -> None:
        self.node_id = node_id

    def request_vote_from_peer(self, candidate_id: str) -> bool:
        # Simplification: nodes grant their vote to the requesting candidate for this test harness
        return True


class ConsensusElectionSimulator:
    """Simulates a cluster election loop and calculates quorum majorities."""
    
    def __init__(self, node_ids: List[str]) -> None:
        self.cluster_nodes = [SimpleConsensusNode(nid) for nid in node_ids]
        self.total_size = len(node_ids)

    def calculate_required_quorum(self) -> int:
        """Calculates the strict majority quorum threshold for the cluster size."""
        return (self.total_size // 2) + 1

    def run_simulated_election(self, candidate_id: str) -> str:
        """Polls the cluster to see if the candidate can reach a quorum majority."""
        votes_secured = 1 # Candidate automatically votes for itself
        quorum_needed = self.calculate_required_quorum()
        
        for peer in self.cluster_nodes:
            if peer.node_id != candidate_id:
                if peer.request_vote_from_peer(candidate_id):
                    votes_secured += 1

        if votes_secured >= quorum_needed:
            return f"ELECTION_SUCCESS: Secured {votes_secured}/{self.total_size} votes. Quorum reached."
        return f"ELECTION_FAILURE: Only secured {votes_secured}/{self.total_size} votes."


if __name__ == "__main__":
    # Initialize a standard 5 node Raft consensus cluster instance setup
    simulator = ConsensusElectionSimulator(["node-A", "node-B", "node-C", "node-D", "node-E"])
    
    required_majority = simulator.calculate_required_quorum()
    print(f"[SIMULATOR] Cluster Count: {simulator.total_size} | Strict Quorum Majority Threshold Needed: {required_majority}")
    
    execution_result = simulator.run_simulated_election("node-A")
    print(f" -> Outcome: {execution_result}")