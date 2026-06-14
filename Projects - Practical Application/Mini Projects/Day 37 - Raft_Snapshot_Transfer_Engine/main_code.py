"""
System: Production-Grade Raft Snapshot Truncation and Transfer Engine
Description: Implements a production-style snapshotting workflow for Raft. When a leader's log 
             grows past a configured threshold, it compacts historical entries into a snapshot 
             and automatically streams it to lagging followers using the InstallSnapshot RPC.
Lead Engineer: Syed Saad Bin Irfan
"""

import json
import logging
from typing import Dict, List, Tuple, Optional

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)s] (SnapshotEngine) %(message)s')

class RaftNodeWithSnapshotSupport:
    """An advanced Raft node capable of compacting its logs and installing raw state snapshots."""
    
    def __init__(self, node_id: str, is_leader: bool = False) -> None:
        self.node_id: str = node_id
        self.is_leader: bool = is_leader
        self.current_term: int = 2
        
        # The primary state store driven by the log stream
        self.kv_store: Dict[str, str] = {}
        self.log: List[Dict[str, any]] = [{"term": 0, "command": "GENESIS"}]
        
        # Tracking markers for log compaction and snapshots
        self.last_included_index: int = 0
        self.last_included_term: int = 0
        self.disk_snapshot_raw: Optional[bytes] = None

    def append_command(self, command: str) -> None:
        """Appends a new entry to the local log and updates the key-value memory store."""
        self.log.append({"term": self.current_term, "command": command})
        # Apply the update to the local state immediately
        if command.startswith("SET "):
            k, v = command[4:].split("=")
            self.kv_store[k.strip()] = v.strip()

    def enforce_log_compaction(self, compact_up_to_index: int) -> None:
        """Compacts the log up to the target index, converting historical entries into a snapshot."""
        if compact_up_to_index >= len(self.log) or compact_up_to_index <= self.last_included_index:
            return

        logging.info(f"[{self.node_id}] Triggering log compaction through index {compact_up_to_index}...")
        
        # Update snapshot metadata boundaries
        self.last_included_term = self.log[compact_up_to_index]["term"]
        self.last_included_index = compact_up_to_index
        
        # Serialize the current state to simulate writing it to disk
        snapshot_payload = {
            "metadata": {"last_included_index": self.last_included_index, "last_included_term": self.last_included_term},
            "state": self.kv_store
        }
        self.disk_snapshot_raw = json.dumps(snapshot_payload).encode('utf-8')
        
        # Truncate the log, preserving a placeholder at index 0 for indexing consistency
        self.log = [{"term": self.last_included_term, "command": "COMPACTED_SNAPSHOT_BOUNDARY"}] + self.log[compact_up_to_index + 1:]
        logging.info(f"[{self.node_id}] Compaction complete. Active log size reduced to {len(self.log)} entries.")

    def dispatch_snapshot_to_peer(self, peer_node: 'RaftNodeWithSnapshotSupport') -> None:
        """Transmits the local snapshot to a lagging peer via a simulated InstallSnapshot RPC."""
        if not self.disk_snapshot_raw:
            return
            
        logging.info(f"[LEADER] Dispatching InstallSnapshot RPC to lagging node '{peer_node.node_id}'...")
        
        # Build the RPC request packet
        rpc_payload = {
            "term": self.current_term,
            "leader_id": self.node_id,
            "last_included_index": self.last_included_index,
            "last_included_term": self.last_included_term,
            "data": self.disk_snapshot_raw
        }
        
        # Route the packet to the follower node
        peer_node.handle_install_snapshot_rpc(rpc_payload)

    def handle_install_snapshot_rpc(self, payload: Dict[str, any]) -> None:
        """Processes an incoming InstallSnapshot RPC, overwriting local state and logs."""
        target_idx = payload["last_included_index"]
        logging.info(f"[{self.node_id}] Received InstallSnapshot RPC from leader. Processing installation...")
        
        # Deserialize the snapshot data block
        unpacked = json.loads(payload["data"].decode('utf-8'))
        
        # Wipe local logs and state, reinitializing directly from the snapshot boundary
        self.kv_store = unpacked["state"]
        self.last_included_index = target_idx
        self.last_included_term = payload["last_included_term"]
        self.log = [{"term": self.last_included_term, "command": "COMPACTED_SNAPSHOT_BOUNDARY"}]
        
        logging.info(f"[{self.node_id}] Snapshot installed successfully. State synced: {self.kv_store}")


if __name__ == "__main__":
    print("\n=== INITIALIZING RAFT SNAPSHOT TRANSFER ENGINE ===\n")
    
    leader_node = RaftNodeWithSnapshotSupport("leader-node-01", is_leader=True)
    lagging_follower = RaftNodeWithSnapshotSupport("follower-node-03", is_leader=False)
    
    # Simulate the leader processing a large stream of updates over time
    leader_node.append_command("SET database_engine=RocksDB")
    leader_node.append_command("SET microservice_status=green")
    leader_node.append_command("SET cluster_region=karachi")
    leader_node.append_command("SET load_balancer_weight=100")
    
    # The leader logs grow large; trigger manual compaction through index 3
    leader_node.enforce_log_compaction(compact_up_to_index=3)
    
    # A lagging follower reconnects and needs to be caught up
    print(f"\n[SYNC-LOOP] Lagging Follower State before sync: {lagging_follower.kv_store}")
    leader_node.dispatch_snapshot_to_peer(lagging_follower)
    
    print(f"\n[POST-SYNC] Verification Check: Follower KV Store = {lagging_follower.kv_store}")
    print("\n=== SYSTEM SHUTDOWN: RAFT SNAPSHOT STORAGE WORKLOAD CLOSED ===")