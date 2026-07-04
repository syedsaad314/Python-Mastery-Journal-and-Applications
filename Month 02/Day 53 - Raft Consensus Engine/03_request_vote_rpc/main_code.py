# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: RequestVote RPC Mechanics
Description: Handles voting requests from candidate nodes, ensuring 
             each node only grants a single vote per logical term.
"""
from typing import Dict, Any

class VoteEvaluationEngine:
    def __init__(self, current_term: int) -> None:
        self.current_term = current_term
        self.voted_for = None

    def handle_vote_request(self, candidate_id: str, candidate_term: int) -> bool:
        if candidate_term > self.current_term:
            self.current_term = candidate_term
            self.voted_for = None

        if candidate_term == self.current_term and (self.voted_for is None or self.voted_for == candidate_id):
            self.voted_for = candidate_id
            return True
            
        return False

if __name__ == "__main__":
    engine = VoteEvaluationEngine(current_term=2)
    # Rejects votes from candidates stuck in older logical terms
    assert engine.handle_vote_request("node_candidate", 1) == False
    # Grants a vote if it hasn't voted yet in the current term
    assert engine.handle_vote_request("node_candidate", 2) == True
    # Rejects subsequent vote requests within the same term
    assert engine.handle_vote_request("competing_candidate", 2) == False