# Lead Engineer: Syed Saad Bin Irfan
"""
Portfolio Layer: Synchronous Packet Backplane Communications Hub
"""
from typing import Dict, List, Any
from models import AppendEntriesRequest, AppendEntriesResponse

class SynchronousNetworkBackplane:
    def __init__(self) -> None:
        self.nodes_registry: Dict[str, Any] = {}

    def register_cluster_target(self, node_id: str, node_instance: Any) -> None:
        self.nodes_registry[node_id] = node_instance

    def route_append_entries(self, target_node_id: str, request: AppendEntriesRequest) -> AppendEntriesResponse:
        target_node = self.nodes_registry[target_node_id]
        return target_node.handle_append_entries_rpc(request)