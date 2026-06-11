"""
Core Topic: Distributed Request Router Gateway
Description: Simulates an API gateway routing write/read requests to the correct shard node.
Lead Engineer: Syed Saad Bin Irfan
"""

from typing import Dict, Optional
from main_code import VirtualNodeHashRing

class RequestRouterGateway:
    """Acts as an API Gateway proxy routing client traffic to specific backend shard instances."""
    
    def __init__(self, ring_topology: VirtualNodeHashRing) -> None:
        self.topology = ring_topology
        # Simulate active memory storage partitions on each server node
        self.nodes_storage_mock: Dict[str, Dict[str, str]] = {
            "node_a": {}, "node_b": {}, "node_c": {}
        }

    def route_write_request(self, key: str, value: str) -> str:
        """Finds the correct server node for a key and saves the value there."""
        target_node = self.topology.get_node(key)
        if target_node and target_node in self.nodes_storage_mock:
            self.nodes_storage_mock[target_node][key] = value
            return target_node
        return "ROUTING_FAILURE"

    def route_read_request(self, key: str) -> Optional[str]:
        """Finds the server node holding a key and reads its value."""
        target_node = self.topology.get_node(key)
        if target_node and target_node in self.nodes_storage_mock:
            return self.nodes_storage_mock[target_node].get(key, "KEY_NOT_FOUND")
        return None


if __name__ == "__main__":
    shared_ring = VirtualNodeHashRing(["node_a", "node_b", "node_c"], vnode_count=100)
    gateway = RequestRouterGateway(shared_ring)
    
    print("[GATEWAY] Intercepting incoming client transactions...")
    n1 = gateway.route_write_request("auth_token", "jwt_token_payload_abc")
    n2 = gateway.route_write_request("config_version", "v2.4.1")
    
    print(f" -> 'auth_token' saved to node: {n1}")
    print(f" -> 'config_version' saved to node: {n2}")
    print(f" -> Reading 'auth_token' value: {gateway.route_read_request('auth_token')}")