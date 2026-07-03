# Lead Engineer: Syed Saad Bin Irfan
"""
Portfolio Layer: Fully Autonomous P2P Cluster Membership Node Engine
"""
import random
from typing import Dict, List, Optional
from models import PeerMetadata, ClusterGossipMessage

class DistributedGossipNode:
    def __init__(self, node_id: str) -> None:
        self.node_id = node_id
        # Internal state repository tracking cluster-wide membership views
        self.membership_registry: Dict[str, Dict[str, Any]] = { # type: ignore
            node_id: {"heartbeat": 0, "status": "ALIVE"}
        }

    def increment_local_heartbeat(self) -> None:
        self.membership_registry[self.node_id]["heartbeat"] += 1

    def compile_gossip_packet(self) -> ClusterGossipMessage:
        return ClusterGossipMessage(
            origin_node_id=self.node_id,
            payload_table={k: v.copy() for k, v in self.membership_registry.items()}
        )

    def select_gossip_peer(self, active_network_nodes: List[str]) -> Optional[str]:
        # Filter target array list down to distinct peer nodes
        candidates = [n for n in active_network_nodes if n != self.node_id]
        if not candidates:
            return None
        return random.choice(candidates)

    def process_incoming_gossip(self, packet: ClusterGossipMessage) -> List[str]:
        """
        Infection Strategy: Evaluates external data states, updating local metrics 
        whenever incoming heartbeat sequences are higher.
        """
        discovered_or_updated_keys: List[str] = []
        
        for peer_id, remote_meta in packet.payload_table.items():
            if peer_id not in self.membership_registry:
                self.membership_registry[peer_id] = remote_meta.copy()
                discovered_or_updated_keys.append(peer_id)
            else:
                local_meta = self.membership_registry[peer_id]
                # Overwrite local state if incoming counter indicates newer history
                if remote_meta["heartbeat"] > local_meta["heartbeat"]:
                    # Preserve 'DEAD' flags if already identified globally
                    if local_meta["status"] != "DEAD":
                        local_meta["heartbeat"] = remote_meta["heartbeat"]
                        local_meta["status"] = remote_meta["status"]
                        discovered_or_updated_keys.append(peer_id)
                        
        return discovered_or_updated_keys

    def execute_anti_entropy_sync(self, target_node: 'DistributedGossipNode') -> None:
        """
        Anti-Entropy: Performs a full, two-way sync loop to guarantee state convergence
        between two specific node registries.
        """
        all_keys = set(self.membership_registry.keys()).union(target_node.membership_registry.keys())
        
        for key in all_keys:
            m1 = self.membership_registry.get(key)
            m2 = target_node.membership_registry.get(key)
            
            if m1 and m2:
                highest_heartbeat = max(m1["heartbeat"], m2["heartbeat"])
                winning_status = m1["status"] if m1["heartbeat"] >= m2["heartbeat"] else m2["status"]
                
                merged_entry = {"heartbeat": highest_heartbeat, "status": winning_status}
                self.membership_registry[key] = merged_entry
                target_node.membership_registry[key] = merged_entry.copy()
            elif m1 and not m2:
                target_node.membership_registry[key] = m1.copy()
            elif m2 and not m1:
                self.membership_registry[key] = m2.copy()

    def audit_and_detect_failures(self, failure_threshold_ticks: int, reference_tick: int) -> List[str]:
        """
        Failure Detection: Identifies nodes that have stopped updating their counters 
        and flags them as DEAD.
        """
        evicted_nodes = []
        for peer_id, meta in self.membership_registry.items():
            if peer_id == self.node_id:
                continue
                
            if meta["status"] == "ALIVE" and (reference_tick - meta["heartbeat"]) > failure_threshold_ticks:
                meta["status"] = "DEAD"
                evicted_nodes.append(peer_id)
        return evicted_nodes