"""
Core Topic: Sloppy Quorum and Hinted Handoff Execution
Description: Diverts write requests to temporary backup nodes when target replicas are down.
Lead Engineer: Syed Saad Bin Irfan
"""

from typing import List, Dict, Tuple

class TargetReplica:
    """Represents a primary storage node that can experience network drops."""
    def __init__(self, node_id: str) -> None:
        self.node_id: str = node_id
        self.is_online: bool = True
        self.data_store: Dict[str, str] = {}


class SecondaryHandoffNode:
    """A nearby backup node that temporarily holds writes for offline primary servers."""
    def __init__(self, node_id: str) -> None:
        self.node_id: str = node_id
        self.handoff_queue: List[Tuple[str, str, str]] = [] # Tracks (TargetNodeID, Key, Value)

    def accept_hinted_write(self, target_node_id: str, key: str, value: str) -> None:
        self.handoff_queue.append((target_node_id, key, value))

    def replay_hints_to_target(self, target_node: TargetReplica) -> None:
        """Flushes and replays all stored updates to the target node once it comes back online."""
        for item in list(self.handoff_queue):
            t_id, k, v = item
            if t_id == target_node.node_id and target_node.is_online:
                target_node.data_store[k] = v
                self.handoff_queue.remove(item)
                print(f"[HANDOFF] Replayed key '{k}' back to primary node '{target_node.node_id}'.")


if __name__ == "__main__":
    primary_node = TargetReplica("primary-database-cell")
    backup_node = SecondaryHandoffNode("neighbor-backup-cell")
    
    # Simulate a network drop on the primary node
    primary_node.is_online = False
    
    print("[INGEST-GATEWAY] Primary node is offline. Diverting write to backup via Sloppy Quorum...")
    if not primary_node.is_online:
        backup_node.accept_hinted_write(primary_node.node_id, "session_404", "UserDataPayload")
        
    # Bring the primary node back online and replay missed updates
    primary_node.is_online = True
    print("[INGEST-GATEWAY] Primary node recovered. Initiating hinted handoff flush...")
    backup_node.replay_hints_to_target(primary_node)