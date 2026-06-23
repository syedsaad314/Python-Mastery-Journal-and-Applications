# Lead Engineer: Syed Saad Bin Irfan
"""
Component: Log Overwrite & Reconciliation Engine
Description: Coordinates pointer backtracking, conflict tracking, and log truncation.
"""

from typing import List

class LogReconciliationEngine:
    @staticmethod
    def synchronize_peer(leader_node, peer_node) -> bool:
        """Forces a peer's history to match the leader's log by finding where they diverge."""
        leader_history = leader_node.storage.history
        match_index = len(peer_node.storage.history) - 1
        
        while match_index >= 0:
            if match_index < len(leader_history):
                if peer_node.storage.history[match_index].term == leader_history[match_index].term:
                    break
            match_index -= 1

        print(f"[RECONCILE] Common match point verified with {peer_node.node_id} at index {match_index}")
        
        peer_node.storage.force_override_history(list(leader_history))
        peer_node.commit_index = leader_node.commit_index
        peer_node.storage.rebuild_state_machine(peer_node.commit_index)
        return True