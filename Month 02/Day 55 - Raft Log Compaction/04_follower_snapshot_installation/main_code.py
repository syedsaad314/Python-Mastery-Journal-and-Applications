# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Follower Snapshot Installation Handling
Description: Processes incoming snapshots on the follower, clearing out 
             outdated local logs and fast-forwarding the node's state.
"""
from typing import List, Dict, Any, NamedTuple

class LogEntry(NamedTuple):
    term: int
    index: int

class FollowerStorageDriver:
    def __init__(self) -> None:
        self.log: List[LogEntry] = [LogEntry(1, 1), LogEntry(1, 2), LogEntry(1, 3)]
        self.committed_state: Dict[str, Any] = {}
        self.commit_index = 0

    def process_install_snapshot(self, last_idx: int, last_term: int, snapshot_data: Dict[str, Any]) -> None:
        # Reset local log; discard any history covered by the snapshot
        self.log = []
        self.commit_index = last_idx
        self.committed_state = snapshot_data.copy()

if __name__ == "__main__":
    driver = FollowerStorageDriver()
    driver.process_install_snapshot(last_idx=5, last_term=2, snapshot_data={"status": "synchronized"})
    assert len(driver.log) == 0
    assert driver.commit_index == 5
    assert driver.committed_state["status"] == "synchronized"