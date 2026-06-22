"""
Core Topic: Participant Transaction State Guard rails
Description: Models how a single database shard locks resources and registers its local vote.
Lead Engineer: Syed Saad Bin Irfan
"""

from enum import Enum, auto

class ParticipantState(Enum):
    READY = auto()
    PREPARED = auto()
    COMMITTED = auto()
    ABORTED = auto()

class ShardParticipantManager:
    """Manages local locks and resource allocations for an isolated database shard."""
    
    def __init__(self, shard_id: str) -> None:
        self.shard_id: str = shard_id
        self.state: ParticipantState = ParticipantState.READY
        self.is_resource_locked: bool = False

    def evaluate_prepare_request(self, balance_check: float, charge_amount: float) -> str:
        """Acquires a local lock and returns a vote based on resource availability."""
        if self.is_resource_locked:
            self.state = ParticipantState.ABORTED
            return "VOTE_ABORT"
            
        if balance_check >= charge_amount:
            self.is_resource_locked = True
            self.state = ParticipantState.PREPARED
            return "VOTE_COMMIT"
        else:
            self.state = ParticipantState.ABORTED
            return "VOTE_ABORT"


if __name__ == "__main__":
    shard = ShardParticipantManager(shard_id="shard-pk-01")
    
    # Simulate evaluating an incoming transaction request
    vote = shard.evaluate_prepare_request(balance_check=15000.0, charge_amount=4500.0)
    print(f"[SHARD-PARTICIPANT] Shard registered local vote: {vote}")
    print(f"[SHARD-PARTICIPANT] Post-prepare state: {shard.state.name} | Resource Lock = {shard.is_resource_locked}")