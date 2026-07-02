# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Anti-Entropy Synchronization
Description: Reconciles state tracking tables symmetrically between two disparate 
             nodes to achieve full cluster consistency.
"""
from typing import Dict, Any

class AntiEntropySynchronizer:
    @staticmethod
    def sync_nodes(node_a_table: Dict[str, Dict[str, Any]], node_b_table: Dict[str, Dict[str, Any]]) -> None:
        # Symmetrical merger strategy matching full state convergence rules
        all_nodes = set(node_a_table.keys()).union(node_b_table.keys())
        for n_id in all_nodes:
            meta_a = node_a_table.get(n_id)
            meta_b = node_b_table.get(n_id)
            
            if meta_a and meta_b:
                target_heartbeat = max(meta_a["heartbeat"], meta_b["heartbeat"])
                chosen_status = meta_a["status"] if meta_a["heartbeat"] >= meta_b["heartbeat"] else meta_b["status"]
                
                node_a_table[n_id] = {"heartbeat": target_heartbeat, "status": chosen_status}
                node_b_table[n_id] = {"heartbeat": target_heartbeat, "status": chosen_status}
            elif meta_a and not meta_b:
                node_b_table[n_id] = meta_a.copy()
            elif meta_b and not meta_a:
                node_a_table[n_id] = meta_b.copy()

if __name__ == "__main__":
    nA = {"node_1": {"heartbeat": 10, "status": "ALIVE"}}
    nB = {"node_1": {"heartbeat": 5, "status": "ALIVE"}, "node_2": {"heartbeat": 1, "status": "ALIVE"}}
    AntiEntropySynchronizer.sync_nodes(nA, nB)
    assert nA["node_1"]["heartbeat"] == 10
    assert nB["node_1"]["heartbeat"] == 10
    assert "node_2" in nA