"""
Core Topic: Physical Clock Skew and Drift Simulator
Description: Demonstrates why physical clocks fail to order distributed transactions safely.
Lead Engineer: Syed Saad Bin Irfan
"""

import time
from typing import List, Dict

class MockPhysicalClusterNode:
    """Simulates a cluster node whose internal clock drifts away from true system time."""
    
    def __init__(self, node_id: str, clock_skew_offset_seconds: float) -> None:
        self.node_id: str = node_id
        self.skew_offset: float = clock_skew_offset_seconds
        self.transaction_log: List[dict] = []

    def get_skewed_timestamp(self) -> float:
        """Returns the node's local timestamp, which includes its unique clock drift."""
        return time.time() + self.skew_offset

    def commit_transaction(self, tx_id: str, payload: str) -> dict:
        """Logs a transaction using the node's local, drifted timestamp."""
        record = {
            "tx_id": tx_id,
            "local_timestamp": self.get_skewed_timestamp(),
            "payload": payload,
            "committed_by": self.node_id
        }
        self.transaction_log.append(record)
        return record


if __name__ == "__main__":
    # Server A's clock is 5 seconds fast; Server B's clock is 5 seconds slow
    server_a = MockPhysicalClusterNode("server-fast", clock_skew_offset_seconds=5.0)
    server_b = MockPhysicalClusterNode("server-slow", clock_skew_offset_seconds=-5.0)
    
    print("[DRIFT-SIM] Simulating real-world transaction execution flow...")
    
    # Step 1: Event occurs on Server B first
    rec_b = server_b.commit_transaction("TX-101", "User Deposited 500 PKR")
    # Step 2: Event occurs on Server A slightly later
    rec_a = server_a.commit_transaction("TX-102", "User Cleared Balance Account")
    
    print(f" -> Event 1 (Happened First) Timestamp: {rec_b['local_timestamp']:.2f}")
    print(f" -> Event 2 (Happened Second) Timestamp: {rec_a['local_timestamp']:.2f}")
    
    if rec_a["local_timestamp"] < rec_b["local_timestamp"]:
        print("[CRITICAL-FAILURE] Physical timestamps show Event 2 happened before Event 1! Data order is corrupted.")