"""
Core Topic: Ring State In-Memory Persistence Tracker
Description: Serializes and restores hash ring topology configurations to preserve ring layout.
Lead Engineer: Syed Saad Bin Irfan
"""

import json
from typing import List, Dict

class RingStateTracker:
    """Saves and restores hash ring cluster layouts using structured JSON configurations."""
    
    @staticmethod
    def export_ring_state(filepath: str, nodes: List[str], vnode_count: int) -> None:
        """Exports the current ring setup to a file."""
        state_payload = {
            "cluster_nodes": nodes,
            "vnode_count": vnode_count,
            "exported_timestamp": 20260608
        }
        with open(filepath, "w") as out_file:
            json.dump(state_payload, out_file, indent=4)
        print(f"[PERSISTENCE] Ring topology layout written to file: '{filepath}'")

    @staticmethod
    def import_ring_state(filepath: str) -> Dict:
        """Loads a saved ring setup from a file to restore the cluster configuration."""
        with open(filepath, "r") as in_file:
            return json.load(in_file)


if __name__ == "__main__":
    target_path = "cluster_ring_state.json"
    active_servers = ["node_10", "node_20", "node_30"]
    
    RingStateTracker.export_ring_state(target_path, active_servers, vnode_count=100)
    restored_config = RingStateTracker.import_ring_state(target_path)
    
    print(f"[PERSISTENCE] Restored Cluster Setup Model: {restored_config['cluster_nodes']}")
    
    import os
    if os.path.exists(target_path):
        os.remove(target_path)