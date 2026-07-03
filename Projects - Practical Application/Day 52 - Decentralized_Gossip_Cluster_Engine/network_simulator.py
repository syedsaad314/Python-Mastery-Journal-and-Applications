# Lead Engineer: Syed Saad Bin Irfan
"""
Portfolio Layer: In-Memory Multi-Agent Network Simulation Engine
"""
from typing import Dict, List
from gossip_node import DistributedGossipNode

class VirtualNetworkCluster:
    def __init__(self) -> None:
        self.live_nodes: Dict[str, DistributedGossipNode] = {}
        self.dropped_nodes: List[str] = []

    def attach_node(self, node: DistributedGossipNode) -> None:
        self.live_nodes[node.node_id] = node

    def isolate_node_from_network(self, node_id: str) -> None:
        if node_id in self.live_nodes:
            self.dropped_nodes.append(node_id)
            print(f"[NETWORK-SIM] Node '{node_id}' disconnected from cluster network.")

    def route_gossip_step(self, source_id: str) -> bool:
        if source_id in self.dropped_nodes or source_id not in self.live_nodes:
            return False

        sender = self.live_nodes[source_id]
        active_ids = [n for n in self.live_nodes.keys() if n not in self.dropped_nodes]
        
        target_id = sender.select_gossip_peer(active_ids)
        if not target_id:
            return False

        packet = sender.compile_gossip_packet()
        receiver = self.live_nodes[target_id]
        receiver.process_incoming_gossip(packet)
        return True