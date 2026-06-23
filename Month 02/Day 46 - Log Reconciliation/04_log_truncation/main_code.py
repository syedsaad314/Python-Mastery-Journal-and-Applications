# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Log Truncation Mechanics
Description: Prunes conflicting data entries from a target index onward to clean a node's log history.
"""

from typing import List, Dict

class LogTruncator:
    @staticmethod
    def truncate_from_index(local_log: List[Dict[str, any]], target_index: int) -> List[Dict[str, any]]:
        if 0 <= target_index < len(local_log):
            print(f"[TRUNCATE] Removing uncommitted entries from index {target_index} to end.")
            local_log = local_log[:target_index]
        return local_log

if __name__ == "__main__":
    corrupted_history = [{"term": 1}, {"term": 1}, {"term": 2}, {"term": 2}]
    cleaned_history = LogTruncator.truncate_from_index(corrupted_history, 2)
    assert len(cleaned_history) == 2