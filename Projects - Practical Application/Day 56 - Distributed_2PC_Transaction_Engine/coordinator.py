# Lead Engineer: Syed Saad Bin Irfan
"""
Portfolio Layer: Centralized Two-Phase Commit Transaction Coordinator
"""
from typing import List, Dict, Any
from models import TransactionPayload, TransactionCommand, ParticipantVote
from network_stub import LatencyAwareNetworkFabric

class TwoPhaseCommitCoordinator:
    def __init__(self, participants: List[str], network: LatencyAwareNetworkFabric) -> None:
        self.participants = participants
        self.network = network
        self.global_tx_history_log: List[str] = []

    def execute_transaction(self, tx_id: str, key: str, value: Any) -> bool:
        print(f"\n[COORDINATOR] Starting Distributed Transaction {tx_id} -> ({key}: {value})")
        self.global_tx_history_log.append(f"TX_START:{tx_id}")
        
        # ---------------------------------------------------------------------
        # PHASE 1: THE VOTING PHASE
        # ---------------------------------------------------------------------
        votes_pool: Dict[str, ParticipantVote] = {}
        prepare_payload = TransactionPayload(tx_id=tx_id, command=TransactionCommand.PREPARE, payload_data={"key": key, "value": value})
        
        for peer in self.participants:
            vote = self.network.dispatch_to_node(peer, prepare_payload)
            votes_pool[peer] = vote
            print(f"[PHASE-1-VOTE] Participant '{peer}' responded with: {vote.value}")

        # Evaluate the gathered votes
        unanimous_commit = True
        for peer in self.participants:
            if votes_pool.get(peer) != ParticipantVote.VOTE_COMMIT:
                unanimous_commit = False
                break

        # ---------------------------------------------------------------------
        # PHASE 2: THE EXECUTION PHASE
        # ---------------------------------------------------------------------
        if unanimous_commit:
            print(f"[COORDINATOR] Unanimous approval achieved! Executing GLOBAL_COMMIT...")
            self.global_tx_history_log.append(f"TX_COMMIT:{tx_id}")
            
            commit_payload = TransactionPayload(tx_id=tx_id, command=TransactionCommand.COMMIT, payload_data={})
            for peer in self.participants:
                self.network.dispatch_to_node(peer, commit_payload)
            return True
        else:
            print(f"[COORDINATOR] Transaction failed validation or timed out. Executing GLOBAL_ABORT...")
            self.global_tx_history_log.append(f"TX_ABORT:{tx_id}")
            
            abort_payload = TransactionPayload(tx_id=tx_id, command=TransactionCommand.ABORT, payload_data={})
            for peer in self.participants:
                self.network.dispatch_to_node(peer, abort_payload)
            return False