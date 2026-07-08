# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Log Compaction Threshold Evaluation
Description: Monitors log sizes and triggers compaction routines once 
             the log length exceeds a specified boundary.
"""
class CompactionGuard:
    def __init__(self, limit: int) -> None:
        self.limit = limit

    def requires_compaction(self, current_log_len: int, current_commit_idx: int) -> bool:
        # Safety constraint: Only compact entries that have already been committed
        return current_log_len > self.limit and current_commit_idx >= self.limit

if __name__ == "__main__":
    guard = CompactionGuard(limit=10)
    # Rejects compaction if logs haven't hit the size limit
    assert guard.requires_compaction(current_log_len=5, current_commit_idx=5) == False
    # Rejects compaction if the entries haven't been committed yet
    assert guard.requires_compaction(current_log_len=12, current_commit_idx=4) == False
    # Triggers compaction when entries are safely committed and past the limit
    assert guard.requires_compaction(current_log_len=12, current_commit_idx=11) == True