"""
Core Topic: RequestVote Serialization Data Format
Description: Handles the structures and validation rules for RequestVote messages.
Lead Engineer: Syed Saad Bin Irfan
"""

from typing import Dict, Any

class VoteRequestSerializer:
    """Formats and validates standard RequestVote RPC parameters for leader elections."""
    
    @staticmethod
    def construct_request(candidate_id: str, term: int, last_log_index: int, last_log_term: int) -> Dict[str, Any]:
        return {
            "candidate_id": candidate_id,
            "term": term,
            "last_log_index": last_log_index,
            "last_log_term": last_log_term
        }

    @staticmethod
    def validate_vote_criteria(local_term: int, request_payload: Dict[str, Any]) -> bool:
        """Determines whether to grant a vote based on incoming term values."""
        # A node only grants its vote if the candidate's term is greater than or equal to its own
        if request_payload["term"] > local_term:
            return True
        return False


if __name__ == "__main__":
    # Create a standardized vote request payload from a candidate node
    rpc_payload = VoteRequestSerializer.construct_request(
        candidate_id="node-05", term=3, last_log_index=14, last_log_term=2
    )
    
    # A follower node evaluates the candidate's request against its local term counter
    vote_granted = VoteRequestSerializer.validate_vote_criteria(local_term=2, request_payload=rpc_payload)
    print(f"[SERIALIZER] Request payload: {rpc_payload}")
    print(f" -> Vote evaluation decision result: {'GRANTED' if vote_granted else 'DENIED'}")