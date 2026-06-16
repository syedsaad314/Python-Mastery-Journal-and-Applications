"""
System: Peer-to-Peer Cooperative Transaction Recovery Simulator
Description: Simulates a 3PC coordinator crashing mid-flight and demonstrates how surviving 
             participants run a cooperative query protocol to resolve transactions safely.
Lead Engineer: Syed Saad Bin Irfan
"""

import logging
from typing import List, Dict, Set

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)s] (CooperativeRecovery) %(message)s')

class Simulated3PCParticipant:
    def __init__(self, node_id: str, state_before_crash: str) -> None:
        self.node_id = node_id
        # State can be: "CAN_COMMIT_VOTED", "PRE_COMMIT_STAGED", "COMMITTED", "ABORTED"
        self.state = state_before_crash

    def handle_peer_inquiry(self) -> str:
        """Returns the node's current internal state to inquiring peers."""
        return self.state

    def apply_cooperative_resolution(self, final_decision: str) -> None:
        """Applies the final cluster decision determined by the cooperative recovery pool."""
        self.state = final_decision
        logging.info(f"[{self.node_id}] Cooperative recovery resolved state to: {self.state}")


class PeerRecoveryEnvironmentSimulator:
    """Coordinates peer-to-peer state collection and applies 3PC recovery rules."""
    
    def __init__(self, surviving_nodes: List[Simulated3PCParticipant]) -> None:
        self.survivors = surviving_nodes

    def run_cooperative_consensus_loop(self) -> str:
        """Queries surviving nodes and uses 3PC recovery rules to resolve the transaction."""
        logging.warning("🚨 [COORDINATOR-CRASH] Central Coordinator went offline. Launching Peer Cooperative Recovery...")
        
        # Step 1: Collect internal states from all surviving nodes
        collected_states: Set[str] = set()
        for peer in self.survivors:
            peer_state = peer.handle_peer_inquiry()
            collected_states.add(peer_state)
            logging.info(f"[RECOVERY-POOL] Inquired peer '{peer.node_id}' reported state: {peer_state}")

        # Step 2: Apply non-blocking 3PC consensus recovery logic
        if "COMMITTED" in collected_states:
            final_resolution = "COMMITTED"
        elif "ABORTED" in collected_states:
            final_resolution = "ABORTED"
        elif "PRE_COMMIT_STAGED" in collected_states:
            # If any node reached pre-commit, every node voted yes; safe to commit
            final_resolution = "COMMITTED"
            logging.info("[RECOVERY-DECISION] At least one peer reached PRE_COMMIT. Safe to execute global COMMIT.")
        else:
            # If no node reached pre-commit, we default to an abort for safety
            final_resolution = "ABORTED"
            logging.warning("[RECOVERY-DECISION] No peer reached PRE_COMMIT. Aborting transaction for cluster safety.")

        # Step 3: Broadcast the final decision to all surviving nodes
        for peer in self.survivors:
            peer.apply_cooperative_resolution(final_resolution)
            
        return final_resolution


if __name__ == "__main__":
    print("\n=== RUNNING PEER-TO-PEER COOPERATIVE RECOVERY SIMULATOR ===\n")
    
    # Scenario: The coordinator crashed, but one shard (node-02) made it to the PRE_COMMIT phase
    surviving_cluster_nodes = [
        Simulated3PCParticipant("node-01", "CAN_COMMIT_VOTED"),
        Simulated3PCParticipant("node-02", "PRE_COMMIT_STAGED"),
        Simulated3PCParticipant("node-03", "CAN_COMMIT_VOTED")
    ]
    
    simulator = PeerRecoveryEnvironmentSimulator(surviving_cluster_nodes)
    resolved_outcome = simulator.run_cooperative_consensus_loop()
    
    print(f"\n[RECOVERY-COMPLETE] Global transaction resolved outcome: {resolved_outcome}")
    print("\n=== SYSTEM SHUTDOWN: COOPERATIVE SIMULATION CORES DISCONNECTED ===")