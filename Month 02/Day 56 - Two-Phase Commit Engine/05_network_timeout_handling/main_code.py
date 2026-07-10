# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Network Timeout Heuristics
Description: Handles situations where participants fail to respond within a 
             configured time window by defaulting to a safe abort state.
"""
from typing import List, Dict, Optional

class TimeoutHeuristicManager:
    @staticmethod
    def collect_votes_with_timeout(expected_peers: List[str], real_responses: Dict[str, str]) -> str:
        for peer in expected_peers:
            if peer not in real_responses:
                # Safety guarantee: If any single node times out, fail safe by aborting the transaction
                return "GLOBAL_ABORT"
        return "GLOBAL_COMMIT" if all(v == "VOTE_COMMIT" for v in real_responses.values()) else "GLOBAL_ABORT"

if __name__ == "__main__":
    peers = ["node_1", "node_2", "node_3"]
    # Node 3 fails to respond (missing from the responses map)
    partial_responses = {"node_1": "VOTE_COMMIT", "node_2": "VOTE_COMMIT"}
    
    decision = TimeoutHeuristicManager.collect_votes_with_timeout(peers, partial_responses)
    assert decision == "GLOBAL_ABORT"