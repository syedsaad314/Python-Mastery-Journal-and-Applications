"""
Core Topic: Raft Election Safety Restrictions
Description: Ensures candidate nodes can only win votes if their logs are up to date.
Lead Engineer: Syed Saad Bin Irfan
"""

class ElectionSafetyGuard:
    def __init__(self, last_log_index: int, last_log_term: int) -> None:
        self.last_log_index = last_log_index
        self.last_log_term = last_log_term

    def evaluate_candidate_log_safety(self, candidate_index: int, candidate_term: int) -> bool:
        """Grants vote only if candidate's log is at least as up-to-date as the voter's log."""
        if candidate_term > self.last_log_term:
            return True
        if candidate_term == self.last_log_term and candidate_index >= self.last_log_index:
            return True
        print("[VOTE-DENIED] Candidate log is out of date. Vote withheld.")
        return False


if __name__ == "__main__":
    voter_guard = ElectionSafetyGuard(last_log_index=15, last_log_term=2)
    # Reject a candidate with an older log index even if the term matches
    assert voter_guard.evaluate_candidate_log_safety(candidate_index=14, candidate_term=2) == False
    # Accept a candidate whose log matches or exceeds the voter's log state
    assert voter_guard.evaluate_candidate_log_safety(candidate_index=16, candidate_term=2) == True