# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Index Backtracking
Description: Replaces brute force log scans with a decrementing pointer to locate consensus points.
"""

class IndexBacktracker:
    def __init__(self, follower_last_index: int) -> None:
        self.next_index_pointer = follower_last_index + 1

    def decrement_search_window(self) -> int:
        if self.next_index_pointer > 0:
            self.next_index_pointer -= 1
        print(f"[BACKTRACK] Moving pointer back. Searching next at log index: {self.next_index_pointer}")
        return self.next_index_pointer

if __name__ == "__main__":
    tracker = IndexBacktracker(follower_last_index=5)
    target_idx = tracker.decrement_search_window()
    assert target_idx == 5