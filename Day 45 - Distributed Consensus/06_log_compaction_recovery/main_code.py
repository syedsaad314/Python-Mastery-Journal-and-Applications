"""
Core Topic: Log Compaction and Snapshotting
Description: Replaces redundant sequential logs with a consolidated snapshot state dictionary.
Lead Engineer: Syed Saad Bin Irfan
"""

from typing import List, Dict

class SnapshotLogCompactor:
    def __init__(self) -> None:
        self.consolidated_state_snapshot: Dict[str, any] = {}

    def compact_historical_logs(self, history_ledger: List[Dict[str, any]]) -> int:
        """Collapses a long list of historical log changes into a single key-value snapshot state."""
        for log_entry in history_ledger:
            command_str = log_entry.get("command", "")
            if "SET" in command_str:
                parts = command_str.replace("SET ", "").split("=")
                if len(parts) == 2:
                    self.consolidated_state_snapshot[parts[0].strip()] = parts[1].strip()
        
        print(f"[COMPACTION] Compacted {len(history_ledger)} entries. Snapshot state: {self.consolidated_state_snapshot}")
        return len(self.consolidated_state_snapshot)


if __name__ == "__main__":
    compactor = SnapshotLogCompactor()
    raw_history = [
        {"term": 1, "command": "SET counter=1"},
        {"term": 1, "command": "SET counter=2"},
        {"term": 2, "command": "SET counter=3"}
    ]
    
    compacted_keys = compactor.compact_historical_logs(raw_history)
    assert compacted_keys == 1
    assert compactor.consolidated_state_snapshot["counter"] == "3"