# Lead Engineer: Syed Saad Bin Irfan
"""
Component: Network Cluster Mesh Router
Description: Intercepts out-of-sync followers and triggers the log reconciliation engine.
"""

from typing import List
from node import ClusterStoreNode # type: ignore
from consensus import LogReconciliationEngine

class NetworkMeshRouter:
    def __init__(self, nodes: List[ClusterStoreNode]) -> None:
        self.nodes = nodes

    def broadcast_leader_write(self, leader: ClusterStoreNode, command: str) -> None:
        """Appends a write command to the leader and replicates it, fixing out-of-sync followers."""
        leader.storage.append_raw_entry(leader.current_term, command)
        leader.commit_index = len(leader.storage.history) - 1
        leader.storage.rebuild_state_machine(leader.commit_index)

        print(f"\n[LEADER-WRITE] Ingested operation '{command}' into Leader log index {leader.commit_index}")

        for node in self.nodes:
            if node.is_leader:
                continue
                
            follower_last_idx = len(node.storage.history) - 1
            if (follower_last_idx < 0 or 
                follower_last_idx != leader.commit_index or 
                node.storage.history[follower_last_idx].term != leader.current_term):
                
                print(f"[MISMATCH] Out-of-sync state caught on node {node.node_id}. Running reconciliation...")
                LogReconciliationEngine.synchronize_peer(leader, node)