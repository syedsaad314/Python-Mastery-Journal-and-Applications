"""
Component: Cluster State Synchronization Manager
Description: Simulates synchronization loops that reconcile token balances across active nodes.
Lead Engineer: Syed Saad Bin Irfan
"""

import threading
from typing import Dict
from rate_bucket import TokenBucketLimiter

class ClusterSynchronizationCoordinator:
    """Manages token level synchronization across independent API gateway nodes."""
    
    def __init__(self, nodes: Dict[str, TokenBucketLimiter]) -> None:
        self.nodes = nodes
        self._lock = threading.Lock()

    def broadcast_global_reconciliation_cycle(self) -> None:
        """Calculates the average token level across the cluster and updates all nodes to match."""
        with self._lock:
            if not self.nodes:
                return

            total_tokens = 0.0
            for node in self.nodes.values():
                with node._lock:
                    total_tokens += node.tokens

            # Compute the cluster-wide synchronized token baseline
            cluster_average = total_tokens / len(self.nodes)

            # Sync all gateway nodes to the calculated baseline level
            for node in self.nodes.values():
                node.synchronize_tokens(cluster_average)