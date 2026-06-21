"""
Core Topic: Consumer Offset Commit Tracking
Description: Tracks and commits reader offsets to guarantee reliable message processing checkpoints.
Lead Engineer: Syed Saad Bin Irfan
"""

from typing import Dict

class ConsumerOffsetTracker:
    """Manages offset checkpoints to pick up from the right spot if a consumer restarts."""
    
    def __init__(self) -> None:
        self._committed_offsets: Dict[str, int] = {}

    def commit_offset(self, topic_partition_key: str, offset: int) -> None:
        """Safely commits the processed offset index for a specific partition."""
        self._committed_offsets[topic_partition_key] = offset
        print(f"[CHECKPOINT] Committed tracking offset key '{topic_partition_key}' at index -> {offset}")

    def get_last_committed(self, topic_partition_key: str) -> int:
        """Returns the last successfully processed offset checkpoint index."""
        return self._committed_offsets.get(topic_partition_key, 0)


if __name__ == "__main__":
    tracker = ConsumerOffsetTracker()
    key = "orders-topic:partition-1"
    
    tracker.commit_offset(key, 104)
    assert tracker.get_last_committed(key) == 104