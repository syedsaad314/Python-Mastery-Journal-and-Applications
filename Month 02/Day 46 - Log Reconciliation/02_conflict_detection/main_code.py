# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Log Conflict Detection
Description: Identifies points where a follower's log diverges in term numbers from the leader's log.
"""

from typing import List, Dict

class ConflictDetector:
    @staticmethod
    def locate_divergence_index(leader_log: List[Dict[str, any]], follower_log: List[Dict[str, any]]) -> int:
        comparison_length = min(len(leader_log), len(follower_log))
        for idx in range(comparison_length):
            if leader_log[idx]["term"] != follower_log[idx]["term"]:
                print(f"[CONFLICT] Divergence caught at log index {idx}. Term mismatch.")
                return idx
        return comparison_length

if __name__ == "__main__":
    leader = [{"term": 1, "cmd": "A"}, {"term": 2, "cmd": "B"}, {"term": 2, "cmd": "C"}]
    follower = [{"term": 1, "cmd": "A"}, {"term": 1, "cmd": "X"}] # Diverges at index 1
    divergence_point = ConflictDetector.locate_divergence_index(leader, follower)
    assert divergence_point == 1