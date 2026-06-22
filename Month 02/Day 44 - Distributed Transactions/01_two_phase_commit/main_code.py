"""
Core Topic: Two-Phase Commit Protocol (2PC)
Description: Models basic prepare and commit/rollback operations across distributed nodes.
Lead Engineer: Syed Saad Bin Irfan
"""

from typing import List

class ParticipantNode:
    def __init__(self, name: str, valid: bool = True) -> None:
        self.name = name
        self.valid = valid

    def prepare(self) -> str:
        return "VOTE_COMMIT" if self.valid else "VOTE_ABORT"


class TwoPhaseCommitCoordinator:
    def __init__(self, participants: List[ParticipantNode]) -> None:
        self.participants = participants

    def execute_transaction(self) -> bool:
        # Phase 1: Prepare Phase
        votes = [p.prepare() for p in self.participants]
        print(f"[2PC-PREPARE] Collected votes: {votes}")
        
        # Phase 2: Commit Phase
        if all(v == "VOTE_COMMIT" for v in votes):
            print("[2PC-COMMIT] Global commit consensus achieved.")
            return True
        print("[2PC-ABORT] Global abort executed due to rejection vote.")
        return False


if __name__ == "__main__":
    nodes = [ParticipantNode("db_node_1", True), ParticipantNode("db_node_2", False)]
    coordinator = TwoPhaseCommitCoordinator(nodes)
    assert coordinator.execute_transaction() == False