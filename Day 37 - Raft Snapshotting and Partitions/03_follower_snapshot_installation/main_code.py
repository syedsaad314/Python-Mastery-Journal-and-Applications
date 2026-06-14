"""
Core Topic: Follower Snapshot Installation Enforcement
Description: Simulates a follower receiving an InstallSnapshot RPC, overwriting its state and truncating logs.
Lead Engineer: Syed Saad Bin Irfan
"""

from typing import List, Dict, Any

class SnapshotInstallingFollower:
    """A follower node capable of wiping its local history and initializing directly from a snapshot."""
    
    def __init__(self, node_id: str) -> None:
        self.node_id = node_id
        self.local_log: List[Dict[str, Any]] = [{"term": 0, "command": "INIT"}]
        self.state_store: Dict[str, Any] = {}
        self.commit_index: int = 0

    def receive_install_snapshot_rpc(self, rpc_payload: Dict[str, Any]) -> bool:
        """Processes an incoming snapshot, handles log matching, or wipes history if entirely out of date."""
        target_idx = rpc_payload["last_included_index"]
        
        # If the follower already has this snapshot index in its log, it just truncates up to that point
        if target_idx < len(self.local_log) and self.local_log[target_idx]["term"] == rpc_payload["last_included_term"]:
            self.local_log = [self.local_log[0]] + self.local_log[target_idx + 1:]
        else:
            # Otherwise, the follower clears its entire log and starts fresh from the snapshot boundary
            self.local_log = [{"term": rpc_payload["last_included_term"], "command": "SNAPSHOT_BOUNDARY_MARKER"}]
            
        # Overwrite the state store directly with the snapshot data
        self.state_store = {"snapshot_loaded": True, "payload_index": target_idx}
        self.commit_index = target_idx
        return True


if __name__ == "__main__":
    follower = SnapshotInstallingFollower("node-follower-03")
    follower.local_log.append({"term": 1, "command": "STALE_OPERATION_1"})
    
    incoming_rpc = {
        "term": 4,
        "leader_id": "node-leader",
        "last_included_index": 50,
        "last_included_term": 3
    }
    
    print(f"[INSTALL-SNAPSHOT] Pre-installation log size metrics: {len(follower.local_log)}")
    follower.receive_install_snapshot_rpc(incoming_rpc)
    print(f"[INSTALL-SNAPSHOT] Post-installation log states: {follower.local_log}")
    print(f"[INSTALL-SNAPSHOT] Follower commit index boundary reset: {follower.commit_index}")