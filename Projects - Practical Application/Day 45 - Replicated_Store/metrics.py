"""
Component: Cluster State Telemetry Panel
Description: Formats and displays cluster status, term counts, and data logs using clean tables.
Lead Engineer: Syed Saad Bin Irfan
"""

from tabulate import tabulate # type: ignore
from typing import List
from node import ClusterConsensusNode

class ClusterMetricsDashboard:
    """Renders tabular views tracking roles, terms, and data records across cluster nodes."""
    
    @staticmethod
    def output_cluster_matrix(nodes: List[ClusterConsensusNode]) -> None:
        print("\n=========================================================================")
        print("          FAULT-TOLERANT REPLICATED STORAGE STATUS MATRIX")
        print("=========================================================================\n")
        
        cluster_rows = []
        for node in nodes:
            state = node.consensus_state
            log_len = len(node.storage.entries_log)
            committed_keys = str(node.storage.state_machine_data)
            
            cluster_rows.append([
                node.node_id,
                state.current_role.upper(),
                f"Term Epoch {state.current_term}",
                f"{log_len} Entries Enqueued",
                f"Commit Index: {state.commit_index}",
                committed_keys if node.storage.state_machine_data else "{}"
            ])
            
        print(tabulate(cluster_rows, headers=["Node ID Coordinate", "Consensus Role", "Term Epoch", "Log Storage Length", "Commit State", "Applied Storage State Data"], tablefmt="presto"))
        print("-" * 73)