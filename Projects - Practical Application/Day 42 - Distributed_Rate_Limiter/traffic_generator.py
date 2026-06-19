"""
Component: Traffic Spike Simulation Runner
Description: Simulates user query streams, transitioning between normal use and heavy spikes.
Lead Engineer: Syed Saad Bin Irfan
"""

import time
import random
from typing import Dict, List
from rate_bucket import TokenBucketLimiter

class TrafficBurstSimulator:
    """Generates synthetic client request spikes to stress-test the rate limiting layer."""
    
    def __init__(self, target_nodes: Dict[str, TokenBucketLimiter]) -> None:
        self.nodes = target_nodes
        self.node_keys = list(target_nodes.keys())
        self.allowed_requests_counter = 0
        self.dropped_requests_counter = 0

    def simulate_traffic_packet(self, intense_spike_mode: bool) -> str:
        """Dispatches a batch of requests across random cluster gateway nodes."""
        # Adjust request density based on the simulated traffic intensity mode
        packet_density = random.randint(15, 30) if intense_spike_mode else random.randint(2, 6)
        
        chosen_node_key = random.choice(self.node_keys)
        target_engine = self.nodes[chosen_node_key]

        for _ in range(packet_density):
            is_allowed = target_engine.evaluate_request(cost=1)
            if is_allowed:
                self.allowed_requests_counter += 1
            else:
                self.dropped_requests_counter += 1
                
        return chosen_node_key