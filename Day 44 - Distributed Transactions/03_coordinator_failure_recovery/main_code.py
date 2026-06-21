"""
Core Topic: Coordinator Crash Recovery Logs
Description: Parses system recovery logs to reconstruct active consensus states after a crash.
Lead Engineer: Syed Saad Bin Irfan
"""

from typing import List, Dict

class RecoveryManager:
    """Rebuilds the active status of transactions by processing persistent system logs."""
    
    @staticmethod
    def rebuild_coordinator_state(log_events: List[Dict[str, str]]) -> str:
        transaction_state = "UNKNOWN"
        for event in log_events:
            status = event.get("status")
            if status == "INIT":
                transaction_state = "ABORT" # Default fallback for incomplete runs
            elif status in ["COMMIT_DECISION", "ABORT_DECISION"]:
                transaction_state = status
        return transaction_state


if __name__ == "__main__":
    interrupted_logs = [
        {"tx_id": "tx-101", "status": "INIT"},
        {"tx_id": "tx-101", "status": "COMMIT_DECISION"}
    ]
    resolved_state = RecoveryManager.rebuild_coordinator_state(interrupted_logs)
    print(f"[RECOVERY] Reconstructed Transaction Target State: {resolved_state}")
    assert resolved_state == "COMMIT_DECISION"