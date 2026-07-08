# Lead Engineer: Syed Saad Bin Irfan
"""
Portfolio Layer: Multi-Agent Packet Routing Fabric Network
"""
from typing import Dict, Any
from models import AppendEntriesRequest, AppendEntriesResponse, InstallSnapshotRequest, InstallSnapshotResponse

class ClusterNetworkFabric:
    def __init__(self) -> None:
        self.registry: Dict[str, Any] = {}

    def register_node(self, node_id: str, node_instance: Any) -> None:
        self.registry[node_id] = node_instance

    def send_append_entries(self, target_id: str, req: AppendEntriesRequest) -> AppendEntriesResponse:
        return self.registry[target_id].handle_append_entries(req)

    def send_install_snapshot(self, target_id: str, req: InstallSnapshotRequest) -> InstallSnapshotResponse:
        return self.registry[target_id].handle_install_snapshot(req)