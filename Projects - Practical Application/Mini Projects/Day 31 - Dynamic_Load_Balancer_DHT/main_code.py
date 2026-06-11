"""
System: Dynamic Load Balancer with Ring Topology
Description: Implements a load balancer using consistent hashing to route client requests
             to an elastic pool of backend servers based on their IP hashes.
Lead Engineer: Syed Saad Bin Irfan
"""

import hashlib
import bisect
import logging
from typing import List, Dict, Optional

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)s] (LB-Ring) %(message)s')

class BackendWorkerNode:
    """Represents an active backend application server processing routed client requests."""
    
    def __init__(self, server_ip: str) -> None:
        self.server_ip: str = server_ip
        self.processed_connections_log: List[str] = []

    def dispatch_connection(self, client_request_id: str) -> None:
        """Logs and processes a connection request assigned to this backend server."""
        self.processed_connections_log.append(client_request_id)


class Layer7ConsistentLoadBalancer:
    """A Layer-7 load balancer that uses consistent hashing to route client traffic to backend servers."""
    
    def __init__(self, vnode_count: int = 80) -> None:
        self.vnode_count = vnode_count
        self.ring_positions: List[int] = []
        self.position_to_server_map: Dict[int, BackendWorkerNode] = {}

    def _hash_ip(self, ip_string: str) -> int:
        return int(hashlib.md5(ip_string.encode('utf-8')).hexdigest(), 16) & 0xFFFFFFFF

    def add_backend_worker(self, worker: BackendWorkerNode) -> None:
        """Registers a backend server and adds its virtual nodes to the load balancer ring."""
        for i in range(self.vnode_count):
            pos = self._hash_ip(f"{worker.server_ip}-worker-vnode-{i}")
            if pos not in self.position_to_server_map:
                bisect.insort(self.ring_positions, pos)
                self.position_to_server_map[pos] = worker
        logging.info(f"[LB-TOPOLOGY] Registered worker server: [{worker.server_ip}] onto active ring.")

    def remove_backend_worker(self, server_ip: str) -> None:
        """Removes a backend server and its virtual nodes from the load balancer ring."""
        targets = [pos for pos, wrk in self.position_to_server_map.items() if wrk.server_ip == server_ip]
        for pos in targets:
            self.ring_positions.remove(pos)
            del self.position_to_server_map[pos]
        logging.info(f"[LB-TOPOLOGY] De-registered worker server: [{server_ip}] from active ring.")

    def forward_client_request(self, client_ip: str, request_id: str) -> str:
        """Hashes the client's IP address to find the closest backend server and routes the request."""
        if not self.ring_positions:
            return "NO_BACKEND_AVAILABLE"
            
        pos = self._hash_ip(client_ip)
        idx = bisect.bisect_right(self.ring_positions, pos)
        if idx == len(self.ring_positions):
            idx = 0
            
        target_worker = self.position_to_server_map[self.ring_positions[idx]]
        target_worker.dispatch_connection(request_id)
        return target_worker.server_ip


if __name__ == "__main__":
    print("\n=== SYSTEM START: LAYER-7 CONSISTENT HASHING LOAD BALANCER ===\n")
    
    load_balancer = Layer7ConsistentLoadBalancer(vnode_count=100)
    
    # Spin up 3 backend servers
    srv_a = BackendWorkerNode("192.168.10.1")
    srv_b = BackendWorkerNode("192.168.10.2")
    srv_c = BackendWorkerNode("192.168.10.3")
    
    load_balancer.add_backend_worker(srv_a)
    load_balancer.add_backend_worker(srv_b)
    load_balancer.add_backend_worker(srv_c)

    # Route traffic from a consistent set of client IPs
    client_ips = ["10.0.0.5", "172.16.25.4", "192.168.1.50", "10.0.0.5"]
    
    print("\n[ROUTING] Processing incoming network connection requests...")
    for idx, client in enumerate(client_ips):
        assigned_to = load_balancer.forward_client_request(client, f"REQ_ID_00{idx}")
        print(f" -> Client IP '{client}' routed directly to backend instance: {assigned_to}")

    # Remove a node to simulate a server failure
    print("\n[SERVER-FAILURE] Simulating a node crash. Removing backend server '192.168.10.2'...")
    load_balancer.remove_backend_worker("192.168.10.2")

    # Re-route the same traffic to verify graceful rebalancing
    print("\n[ROUTING] Re-routing traffic across remaining backend servers...")
    for idx, client in enumerate(client_ips):
        assigned_to = load_balancer.forward_client_request(client, f"REQ_ID_POST_FAIL_00{idx}")
        print(f" -> Client IP '{client}' now routed to backend instance: {assigned_to}")

    print("\n=== SYSTEM SHUTDOWN: LOAD BALANCER COMPLETED ===")