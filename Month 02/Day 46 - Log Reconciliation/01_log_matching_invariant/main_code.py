# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Log Matching Invariant
Description: Verifies that if two logs contain an entry with the same index and term, they are identical.
"""

from typing import List, Dict

class LogInvariantValidator:
    @staticmethod
    def verify_matching_property(log_a: List[Dict[str, any]], log_b: List[Dict[str, any]], check_index: int) -> bool:
        if check_index >= len(log_a) or check_index >= len(log_b):
            return False
        entry_a = log_a[check_index]
        entry_b = log_b[check_index]
        return entry_a["term"] == entry_b["term"] and entry_a["command"] == entry_b["command"]

if __name__ == "__main__":
    cluster_log_1 = [{"term": 1, "command": "SET x=5"}, {"term": 2, "command": "SET y=10"}]
    cluster_log_2 = [{"term": 1, "command": "SET x=5"}, {"term": 2, "command": "SET y=10"}]
    assert LogInvariantValidator.verify_matching_property(cluster_log_1, cluster_log_2, 1) == True