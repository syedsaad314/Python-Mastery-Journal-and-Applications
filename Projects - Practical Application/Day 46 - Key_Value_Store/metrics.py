# Lead Engineer: Syed Saad Bin Irfan
"""
Component: System Telemetry Monitoring Panel
Description: Formats and displays node logs and key-value states in scannable console tables.
"""

from tabulate import tabulate # type: ignore
from typing import List
from node import ClusterStoreNode

class StorageTelemetryPanel:
    @staticmethod
    def render_cluster_state(nodes: List[ClusterStoreNode]) -> None:
        print("\n" + "="*85)
        print("         DISTRIBUTED LOG RECONCILIATION & REPLICATION SYSTEM MATRIX")
        print("="*85 + "\n")
        
        matrix_rows = []
        for node in nodes:
            log_visual = " | ".join([f"[{i}:T{e.term}]" for i, e in enumerate(node.storage.history)])
            if not log_visual:
                log_visual = "[EMPTY LOG]"
                
            matrix_rows.append([
                node.node_id,
                "LEADER" if node.is_leader else "FOLLOWER",
                f"Term {node.current_term}",
                f"Commit Idx: {node.commit_index}",
                log_visual,
                str(node.storage.memory_state)
            ])
            
        print(tabulate(matrix_rows, headers=["Node Identifier", "Cluster Role", "Term Epoch", "Commit Index", "Log Entry History Array Layout", "Active KV Memory State"], tablefmt="presto"))
        print("-" * 85)