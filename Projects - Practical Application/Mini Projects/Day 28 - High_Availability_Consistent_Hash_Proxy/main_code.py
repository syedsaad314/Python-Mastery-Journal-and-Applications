"""
System: High-Availability Consistent-Hashing Reverse Proxy Load Balancer
Description: A high-performance asynchronous reverse proxy core that maps incoming data traffic
             uniformly across backend node pools using consistent hashing rings and virtual replicas.
Lead Engineer: Syed Saad Bin Irfan
"""

import asyncio
import hashlib
import logging
from typing import Dict, List, Optional

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)s] (Hash-Proxy-Core) %(message)s')

class LoadBalancerHashProxy:
    """Asynchronous routing gateway proxy that load balances traffic using consistent hashing."""
    
    def __init__(self, virtual_nodes_allocation: int = 3) -> None:
        self.replicas = virtual_nodes_allocation
        self.ring_positions_index: List[int] = []
        self.hash_to_physical_node_registry: Dict[int, str] = {}
        self.active_healthy_backends: List[str] = []

    def _hash_to_32bit_integer(self, key_string: str) -> int:
        return int(hashlib.md5(key_string.encode('utf-8')).hexdigest(), 16) & 0xFFFFFFFF

    def register_backend_host(self, host_descriptor_id: str) -> None:
        """Injects a physical server endpoint alongside its virtual tracking rings into the proxy map."""
        logging.info(f"[PROXY] Registering new backend service node: '{host_descriptor_id}'")
        self.active_healthy_backends.append(host_descriptor_id)
        
        for i in range(self.replicas):
            virtual_key = f"{host_descriptor_id}-replica-channel-{i}"
            position_hash = self._hash_to_32bit_integer(virtual_key)
            
            self.hash_to_physical_node_registry[position_hash] = host_descriptor_id
            self.ring_positions_index.append(position_hash)
            
        self.ring_positions_index.sort()

    def route_request_context(self, incoming_client_route_key: str) -> Optional[str]:
        """Maps client route paths straight to the closest clockwise backend service node on the ring."""
        if not self.ring_positions_index:
            return None
            
        request_hash = self._hash_to_32bit_integer(incoming_client_route_key)
        
        # Binary search (bisect left execution metrics) to locate target nodes positions
        low, high = 0, len(self.ring_positions_index) - 1
        target_index = 0
        
        while low <= high:
            mid = (low + high) // 2
            if self.ring_positions_index[mid] >= request_hash:
                target_index = mid
                high = mid - 1
            else:
                low = mid + 1
                
        if low > len(self.ring_positions_index) - 1:
            target_index = 0
            
        assigned_target_host = self.hash_to_physical_node_registry[self.ring_positions_index[target_index]]
        return assigned_target_host

    async def execute_health_monitor_pass(self) -> None:
        """Simulates background daemon checks to prune offline hosts from the routing ring."""
        logging.info("[MONITOR] Launching background telemetry health check passes...")
        # Production extension logic: connect via async sockets to check loop interface health statuses
        await asyncio.sleep(0.01)


if __name__ == "__main__":
    print("\n=== SYSTEM START: HIGH AVAILABILITY REVERSE PROXY CORE ===\n")
    
    proxy_gateway = LoadBalancerHashProxy(virtual_nodes_allocation=4)
    proxy_gateway.register_backend_host("SERVER_POOL_NODE_01")
    proxy_gateway.register_backend_host("SERVER_POOL_NODE_02")
    proxy_gateway.register_backend_host("SERVER_POOL_NODE_03")

    # Simulate routing client requests based on unique session keys
    test_sessions = ["saad_client_token", "fabha_client_token", "ubit_datacenter_route"]
    
    print("\nExecuting Consistent Request Hashing Target Routes:")
    print("-" * 65)
    for session in test_sessions:
        target_server = proxy_gateway.route_request_context(session)
        print(f" Request Session Context: [{session:<22}] -> Routed to: {target_server}")
    print("-" * 65)