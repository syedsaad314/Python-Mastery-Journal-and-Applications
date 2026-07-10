# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Two-Phase Commit Voting Consensus Logic
Description: Evaluates participant votes during Phase 1 to decide 
             whether a global transaction can safely proceed to a commit.
"""
from typing import Dict

class VotingPhaseEngine:
    @staticmethod
    def evaluate_votes(participant_votes: Dict[str, str]) -> bool:
        if not participant_votes:
            return False
            
        # The transaction can only commit if EVERY participant explicitly votes VOTE_COMMIT
        return all(vote == "VOTE_COMMIT" for vote in participant_votes.values())

if __name__ == "__main__":
    # Unanimous agreement case
    unanimous = {"node_A": "VOTE_COMMIT", "node_B": "VOTE_COMMIT"}
    assert VotingPhaseEngine.evaluate_votes(unanimous) == True

    # Dissent case
    dissent = {"node_A": "VOTE_COMMIT", "node_B": "VOTE_ABORT"}
    assert VotingPhaseEngine.evaluate_votes(dissent) == False