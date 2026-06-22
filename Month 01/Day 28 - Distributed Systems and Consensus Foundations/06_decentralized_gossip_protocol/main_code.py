"""
Core Topic: Decentralized Gossip Protocol Topology
Description: Propagates membership tracking updates across peer nodes using randomized gossip sweeps.
Lead Engineer: Syed Saad Bin Irfan
"""

import random
from typing import Dict, Any, List

class GossipClusterMember:
    """Simulates a single cluster node propagating metadata configurations via peer gossip sweeps."""
    
    def __init__(self, node_id: str, known_peers_list: List[str]) -> None:
        self.node_id: str = node_id
        self.peers: List[str] = known_peers_list
        # Track node states along with internal version counter tags
        self.membership_registry: Dict[str, Dict[str, Any]] = {
            node_id: {"status": "ALIVE", "version_tag": 1}
        }

    def trigger_local_state_mutation(self, cluster_target_node: str, new_status: str) -> None:
        """Mutates tracking status properties, advancing version counters to flag updates."""
        current_version = self.membership_registry.get(cluster_target_node, {}).get("version_tag", 0)
        self.membership_registry[cluster_target_node] = {
            "status": new_status,
            "version_tag": current_version + 1
        }

    def compile_gossip_digest(self) -> Dict[str, Dict[str, Any]]:
        return dict(self.membership_registry)

    def receive_gossip_digest(self, incoming_digest: Dict[str, Dict[str, Any]]) -> None:
        """Parses an incoming gossip digest, merging states if the version tag is newer."""
        for node_id, remote_metadata in incoming_digest.items():
            local_metadata = self.membership_registry.get(node_id, None)
            
            if not local_metadata or remote_metadata["version_tag"] > local_metadata["version_tag"]:
                # Accept incoming state update because its tracking code is newer
                self.membership_registry[node_id] = remote_metadata
                print(f"[{self.node_id}] Registry sync update applied: '{node_id}' is now {remote_metadata['status']}")

    def select_random_gossip_target(self) -> Optional[str]: # type: ignore
        if not self.peers:
            return None
        return random.choice(self.peers)


if __name__ == "__main__":
    print("[GOSSIP] Initializing peer-to-peer metadata replication networks...")
    
    # Establish separate node instances tracking each other across the pool entries
    node_alpha = GossipClusterMember("NODE_ALPHA", ["NODE_BETA"])
    node_beta  = GossipClusterMember("NODE_BETA", ["NODE_ALPHA"])

    print("[GOSSIP] Altering cluster state value configuration rules on Node Alpha...")
    node_alpha.trigger_local_state_mutation("NODE_GAMMA", "CRITICAL_FAULT_OFFLINE")
    
    digest_payload = node_alpha.compile_gossip_digest()
    
    print("[GOSSIP] Dispatching randomized gossip digest payload across network paths...")
    node_beta.receive_gossip_digest(digest_payload)