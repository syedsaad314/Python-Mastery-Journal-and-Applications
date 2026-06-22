"""
Core Topic: Replicated State Machine Commit Loops
Description: Takes committed log entries and executes them sequentially against an isolated key-value store.
Lead Engineer: Syed Saad Bin Irfan
"""

from typing import List, Dict

class ReplicatedKVStateMachine:
    """An isolated data store driven sequentially by verified, committed log entries."""
    
    def __init__(self) -> None:
        self.state_store: Dict[str, str] = {}
        self.last_applied_index: int = 0

    def apply_committed_logs(self, log_entries: List[dict], target_commit_index: int) -> int:
        """Applies committed log entries sequentially up to the target commit index."""
        while self.last_applied_index < target_commit_index:
            self.last_applied_index += 1
            entry = log_entries[self.last_applied_index]
            command: str = entry["command"]
            
            # Simple state machine parser execution route
            if command.startswith("SET "):
                parts = command[4:].split("=")
                if len(parts) == 2:
                    self.state_store[parts[0].strip()] = parts[1].strip()
                    
        return self.last_applied_index


if __name__ == "__main__":
    replicated_log = [
        {"term": 0, "command": "GENESIS"},
        {"term": 1, "command": "SET name=saad"},
        {"term": 2, "command": "SET role=engineer"},
        {"term": 2, "command": "SET track=distributed_systems"} # Not yet committed
    ]
    
    kv_store = ReplicatedKVStateMachine()
    
    # Cluster consensus moves the safety commit mark up to index 2
    kv_store.apply_committed_logs(replicated_log, target_commit_index=2)
    
    print(f"[STATE-MACHINE] Engine memory state store dump: {kv_store.state_store}")
    print(f"[STATE-MACHINE] Last applied entry log index location: {kv_store.last_applied_index}")