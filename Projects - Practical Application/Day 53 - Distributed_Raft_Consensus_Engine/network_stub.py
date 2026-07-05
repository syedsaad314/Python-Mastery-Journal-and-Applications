# Lead Engineer: Syed Saad Bin Irfan
"""
Portfolio Layer: In-Memory Simulated Network Routing Backplane
"""
from typing import Dict, List, Any
from models import VoteRequest, VoteResponse, AppendEntriesHeartbeat

class MockNetworkBackplane:
    def __init__(self) -> None:
        self.registry: Dict[str, Any] = {}

    def register_node_instance(self, node_id: str, node_instance: Any) -> None:
        self.registry[node_id] = node_instance

    def broadcast_vote_request(self, sender_id: str, request: VoteRequest) -> List[VoteResponse]:
        responses = []
        for n_id, target_node in self.registry.items():
            if n_id == sender_id:
                continue
            res = target_node.receive_vote_rpc(request)
            responses.append(res)
        return responses

    def broadcast_heartbeat(self, sender_id: str, heartbeat: AppendEntriesHeartbeat) -> None:
        for n_id, target_node in self.registry.items():
            if n_id == sender_id:
                continue
            target_node.receive_heartbeat_rpc(heartbeat)