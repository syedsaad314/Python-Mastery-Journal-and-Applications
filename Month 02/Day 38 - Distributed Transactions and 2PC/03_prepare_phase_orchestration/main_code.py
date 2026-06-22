"""
Core Topic: Two-Phase Commit - Phase 1: Prepare Phase
Description: Simulates a coordinator broadcasting prepare requests and collecting votes.
Lead Engineer: Syed Saad Bin Irfan
"""

from typing import List, Dict

class MockShard:
    def __init__(self, node_id: str, will_vote_yes: bool) -> None:
        self.node_id = node_id
        self.will_vote_yes = will_vote_yes

    def receive_prepare(self) -> str:
        return "VOTE_COMMIT" if self.will_vote_yes else "VOTE_ABORT"

class TwoPhaseCommitOrchestrator:
    """Handles Phase 1 of the 2PC protocol by pulling votes from all registered shards."""
    
    def __init__(self, shards: List[MockShard]) -> None:
        self.shards = shards

    def execute_prepare_phase(self) -> Dict[str, str]:
        """Polls every participant shard for its transaction vote allocation."""
        vote_registry: Dict[str, str] = {}
        
        for shard in self.shards:
            try:
                # Simulate a network RPC invocation pulling a vote payload
                vote_registry[shard.node_id] = shard.receive_prepare()
            except Exception:
                vote_registry[shard.node_id] = "VOTE_ABORT" # Timeout fallback defaults to abort
                
        return vote_registry


if __name__ == "__main__":
    cluster_shards = [MockShard("shard-khi", will_vote_yes=True), MockShard("shard-dxb", will_vote_yes=True)]
    orchestrator = TwoPhaseCommitOrchestrator(cluster_shards)
    
    collected_votes = orchestrator.execute_prepare_phase()
    print(f"[PREPARE-PHASE] Voting summary registry results: {collected_votes}")