# Lead Engineer: Syed Saad Bin Irfan
"""
Portfolio Layer: Synchronous Network Bus Router Simulating Latency & Timeouts
"""
from typing import Dict, Any, Optional
from models import TransactionPayload, ParticipantVote

class LatencyAwareNetworkFabric:
    def __init__(self) -> None:
        self.registered_nodes: Dict[str, Any] = {}
        self.blacklisted_nodes: set[str] = set()

    def register_participant(self, node_id: str, instance: Any) -> None:
        self.registered_nodes[node_id] = instance

    def simulate_network_partition(self, node_id: str) -> None:
        self.blacklisted_nodes.add(node_id)

    def clear_partitions(self) -> None:
        self.blacklisted_nodes.clear()

    def dispatch_to_node(self, target_node_id: str, msg: TransactionPayload) -> ParticipantVote:
        if target_node_id in self.blacklisted_nodes:
            # Simulate a network timeout drop
            return ParticipantVote.TIMEOUT
            
        return self.registered_nodes[target_node_id].receive_transaction_rpc(msg)