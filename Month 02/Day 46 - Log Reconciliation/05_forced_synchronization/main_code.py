# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Forced Log Synchronization
Description: Replaces uncommitted conflicting log indexes with valid entries from the leader.
"""

from typing import List, Dict

class ForcedLogSynchronizer:
    @staticmethod
    def sync_follower_slice(follower_log: List[Dict[str, any]], leader_entries: List[Dict[str, any]], start_idx: int) -> List[Dict[str, any]]:
        follower_log = follower_log[:start_idx]
        follower_log.extend(leader_entries)
        return follower_log

if __name__ == "__main__":
    f_log = [{"term": 1, "val": "X"}, {"term": 1, "val": "Y"}]
    l_entries = [{"term": 2, "val": "Z"}]
    updated_log = ForcedLogSynchronizer.sync_follower_slice(f_log, l_entries, 1)
    assert len(updated_log) == 2
    assert updated_log[1]["term"] == 2