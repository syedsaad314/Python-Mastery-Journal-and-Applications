"""
Core Topic: Raft Consensus Safety Invariants
Description: Implements critical validation checks to protect log consistency during leader elections.
Lead Engineer: Syed Saad Bin Irfan
"""

from typing import List, Tuple

class ConsensusSafetyEvaluator:
    """Validates election logic rules to protect committed historical records across terms."""

    @staticmethod
    def is_candidate_log_up_to_date(voter_log: List[Tuple[int, str]], candidate_last_index: int, candidate_last_term: int) -> bool:
        """Enforces the Election Safety Invariant to ensure candidates have an up-to-date log history."""
        voter_last_index = len(voter_log) - 1
        voter_last_term = voter_log[voter_last_index][0]

        # Rule 1: Compare terms. The candidate with the higher term is more up-to-date
        if candidate_last_term != voter_last_term:
            return candidate_last_term > voter_last_term

        # Rule 2: If terms match, the node with the longer log history is more up-to-date
        return candidate_last_index >= voter_last_index


if __name__ == "__main__":
    print("[SAFETY-INVARIANTS] Running validation checks over conflicting log configurations...")
    
    # Mocking standard voter node log state: [(term, payload)]
    voter_history = [(1, "INIT"), (2, "WRITE_A"), (2, "WRITE_B")]
    
    # Case A: Candidate has a shorter history in an older term
    case_a_verdict = ConsensusSafetyEvaluator.is_candidate_log_up_to_date(
        voter_log=voter_history, 
        candidate_last_index=1, 
        candidate_last_term=1
    )
    print(f"[SAFETY-INVARIANTS] Case A Verdict (Should be False): {case_a_verdict}")

    # Case B: Candidate has a longer history from a more recent term
    case_b_verdict = ConsensusSafetyEvaluator.is_candidate_log_up_to_date(
        voter_log=voter_history, 
        candidate_last_index=4, 
        candidate_last_term=3
    )
    print(f"[SAFETY-INVARIANTS] Case B Verdict (Should be True): {case_b_verdict}")