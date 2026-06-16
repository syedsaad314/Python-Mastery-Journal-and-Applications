"""
Core Topic: Peer-to-Peer Cooperative Recovery Protocol
Description: Simulates participants polling each other to resolve states when a coordinator crashes.
Lead Engineer: Syed Saad Bin Irfan
"""

from typing import List, Set

class RecoveringPeerNode:
    def __init__(self, node_id: str, state: str) -> None:
        self.node_id = node_id
        self.state = state # CAN_COMMIT, PRE_COMMIT, COMMITTED, ABORTED

class PeerCooperativeRecoveryCoordinator:
    """Resolves pending transactions by evaluating states across surviving peer nodes."""
    
    @staticmethod
    def evaluate_peer_states_and_resolve(surviving_peers: List[RecoveringPeerNode]) -> str:
        """Applies 3PC cooperative recovery rules to determine the correct transaction outcome."""
        observed_states: Set[str] = {peer.state for peer in surviving_peers}
        
        # Rule A: If any peer has already committed, the entire cluster must commit
        if "COMMITTED" in observed_states:
            return "RESOLVE_GLOBAL_COMMIT"
            
        # Rule B: If any peer has aborted, the entire cluster must abort
        if "ABORTED" in observed_states:
            return "RESOLVE_GLOBAL_ABORT"
            
        # Rule C: If at least one peer reached PRE_COMMIT, every node voted yes; safe to commit
        if "PRE_COMMIT" in observed_states:
            return "RESOLVE_GLOBAL_COMMIT"
            
        # Rule D: If no node reached PRE_COMMIT, it's not safe to guess; default to abort
        return "RESOLVE_GLOBAL_ABORT"


if __name__ == "__main__":
    # Scenario: Coordinator crashed, but one surviving peer made it to the PRE_COMMIT phase
    survivors = [
        RecoveringPeerNode("peer-A", "CAN_COMMIT"),
        RecoveringPeerNode("peer-B", "PRE_COMMIT"),
        RecoveringPeerNode("peer-C", "CAN_COMMIT")
    ]
    
    resolution = PeerCooperativeRecoveryCoordinator.evaluate_peer_states_and_resolve(survivors)
    print(f"[COOPERATIVE-RECOVERY] Peer-to-peer resolution decision: {resolution}")