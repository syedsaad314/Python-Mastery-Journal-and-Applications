# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Snapshot Recovery Cost Benchmarking
Description: Measures performance gains achieved by restoring system state 
             from structured snapshots instead of replaying thousands of raw logs.
"""
import time
from typing import List

class SnapshotRecoveryBenchmarker:
    def __init__(self) -> None:
        # Simulate a deep history log of 10,000 distinct incremental updates
        self.raw_event_stream: List[int] = [1] * 10000
        self.cached_snapshot_state = 9900
        self.snapshot_version_marker = 9900

    def restore_via_full_replay(self) -> float:
        start = time.perf_counter()
        current_balance = 0
        for amt in self.raw_event_stream:
            current_balance += amt
        return time.perf_counter() - start

    def restore_via_snapshot_checkpoint(self) -> float:
        start = time.perf_counter()
        current_balance = self.cached_snapshot_state
        # Only replay the few trailing events recorded AFTER the snapshot marker version
        for amt in self.raw_event_stream[self.snapshot_version_marker:]:
            current_balance += amt
        return time.perf_counter() - start

if __name__ == "__main__":
    bench = SnapshotRecoveryBenchmarker()
    t_full = bench.restore_via_full_replay()
    t_snap = bench.restore_via_snapshot_checkpoint()
    assert t_snap < t_full
    print(f"[RECOVERY BENCH] Full Replay: {t_full:.5f}s | Optimized Snapshot: {t_snap:.5f}s")