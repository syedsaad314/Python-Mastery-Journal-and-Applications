"""
Core Topic: Distributed Log Replication Appends
Description: Simulates a leader replicating append-only commands to follower log ledgers.
Lead Engineer: Syed Saad Bin Irfan
"""

from typing import List, Dict

class FollowerLogSpace:
    def __init__(self) -> None:
        self.local_log: List[Dict[str, any]] = []

    def handle_append_entries(self, entries: List[Dict[str, any]]) -> bool:
        """Appends new entries received from a validated cluster leader to the local log."""
        for entry in entries:
            self.local_log.append(entry)
        return True


if __name__ == "__main__":
    follower = FollowerLogSpace()
    mock_leader_entries = [{"term": 1, "command": "SET x=10"}, {"term": 1, "command": "SET y=20"}]
    
    success = follower.handle_append_entries(mock_leader_entries)
    assert success is True
    assert len(follower.local_log) == 2