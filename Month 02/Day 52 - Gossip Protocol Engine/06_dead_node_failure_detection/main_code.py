# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Failure Detection Mechanics
Description: Audits the cluster table to mark lagging nodes as DEAD if their 
             heartbeat gaps cross a specified threshold.
"""
from typing import Dict, Any

class FailureDetectorAuditor:
    @staticmethod
    def audit_cluster_liveness(membership_table: Dict[str, Dict[str, Any]], current_virtual_time: int, max_gap: int) -> None:
        for node_id, meta in membership_table.items():
            # In a real system, we cross-reference local time vs last updated timestamp
            if meta["status"] == "ALIVE" and (current_virtual_time - meta["heartbeat"]) > max_gap:
                meta["status"] = "DEAD"
                print(f"[AUDITOR] Marked unresponsive node '{node_id}' as DEAD.")

if __name__ == "__main__":
    table = {"node_failed": {"heartbeat": 2, "status": "ALIVE"}, "node_good": {"heartbeat": 9, "status": "ALIVE"}}
    FailureDetectorAuditor.audit_cluster_liveness(table, current_virtual_time=10, max_gap=5)
    assert table["node_failed"]["status"] == "DEAD"
    assert table["node_good"]["status"] == "ALIVE"