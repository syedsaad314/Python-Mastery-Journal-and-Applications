"""
System: Partition-Resilient Consensus-Backed Key-Value Database Store
Description: A high-fidelity distributed database tracking in-memory transactions via non-blocking
             asyncio frameworks, featuring consensus leader states and strict write quorum validations.
Lead Engineer: Syed Saad Bin Irfan
"""

import asyncio
import json
import logging
from typing import Dict, List, Set, Any, Optional

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)s] (Consensus-Store-Core) %(message)s')

class DatabaseClusterNode:
    """Manages asynchronous state records and communication pipelines for a cluster node."""
    
    def __init__(self, node_id: str, peers_pool: Set[str]) -> None:
        self.node_id: str = node_id
        self.peers: Set[str] = peers_pool
        self.storage_map: Dict[str, Any] = {}
        self.current_role: str = "FOLLOWER"  # FOLLOWER, LEADER
        self.cluster_size: int = len(peers_pool) + 1
        self.majority_quorum: int = (self.cluster_size // 2) + 1
        
    async def process_rpc_append_entry(self, key: str, value: Any) -> bool:
        """Processes transactional mutation inputs dispatched across routing channels."""
        logging.info(f"[{self.node_id}] RPC Mutation validation check triggered over key: '{key}'")
        self.storage_map[key] = value
        return True

    async def execute_distributed_write(self, key: str, value: Any) -> bool:
        """Orchestrates multi-node transactions, verifying write quorums before committing values."""
        if self.current_role != "LEADER":
            logging.warning(f"[{self.node_id}] Write transaction rejected: Node is not the authorized LEADER.")
            return False

        logging.info(f"[{self.node_id}] Initializing distributed transactional consensus stream: {key} -> {value}")
        successful_commit_votes = 1  # Vote for self allocation
        
        # Dispatch parallel compilation commands down peer node channels
        async_worker_tasks = []
        for peer_id in self.peers:
            # Simulated network routing loop abstraction
            async_worker_tasks.append(self._mock_peer_network_call(peer_id, key, value))
            
        execution_outcomes = await asyncio.gather(*async_worker_tasks, return_exceptions=True)
        
        for outcome in execution_outcomes:
            if outcome is True:
                successful_commit_votes += 1

        logging.info(f"[{self.node_id}] Cluster vote consensus outcome: {successful_commit_votes}/{self.cluster_size} (Req: {self.majority_quorum})")
        
        if successful_commit_votes >= self.majority_quorum:
            # Commit the value to local storage safely once quorum is confirmed
            self.storage_map[key] = value
            logging.info(f"[{self.node_id}] TRANSACTION SUCCESS: Key '{key}' committed across quorum boundaries.")
            return True
            
        logging.critical(f"[{self.node_id}] TRANSACTION ABORTED: Quorum verification parameters unfulfilled.")
        return False

    async def _mock_peer_network_call(self, peer_host_id: str, target_key: str, payload_value: Any) -> bool:
        """Simulates low-overhead, non-blocking asynchronous data transfers across network lines."""
        await asyncio.sleep(0.05)  # Simulate network latency
        # Simple simulation hack: assume everything goes through unless explicit failure markers are tripped
        if "FAULT" in peer_host_id:
            return False
        return True


if __name__ == "__main__":
    print("\n=== SYSTEM START: PARTITION-RESILIENT REPLICATED DATASTORE ===\n")
    
    async def main_orchestration_test():
        # Setup an isolated 3-node cluster topology map
        cluster_peers = {"DATANODE_B", "DATANODE_C_FAULT"}
        master_node = DatabaseClusterNode("DATANODE_A_LEADER", cluster_peers)
        master_node.current_role = "LEADER"

        # Case 1: Execute write transactions while cluster connectivity meets quorum requirements
        print("[RUN] Dispatching write transaction 1 (Quorum target should match)...")
        tx_1_status = await master_node.execute_distributed_write("saad_profile_id", {"role": "STAFF_ENGINEER"})
        print(f"[RUN] Transaction status outcome: {tx_1_status}\n")

        # Case 2: Severe network partition isolates backing nodes, dropping connectivity below quorum limits
        print("--- Simulating Network Split-Brain Partition Shock ---")
        master_node.peers = {"DATANODE_B_FAULT", "DATANODE_C_FAULT"} # Both peer links dropped
        
        print("[RUN] Dispatching write transaction 2 (Quorum target should fail)...")
        tx_2_status = await master_node.execute_distributed_write("restricted_financial_ledger_root", 50000)
        print(f"[RUN] Transaction status outcome: {tx_2_status}")

    asyncio.run(main_orchestration_test())