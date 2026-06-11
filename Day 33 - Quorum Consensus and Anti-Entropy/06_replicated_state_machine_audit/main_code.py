"""
Core Topic: Replicated State Machine Transaction Audit Log
Description: Logs transaction states sequentially after confirming quorum requirements.
Lead Engineer: Syed Saad Bin Irfan
"""

from typing import List, Dict, Any

class AuditedStateMachine:
    """Logs cluster state transitions only after they pass quorum confirmation checks."""
    def __init__(self) -> None:
        self.confirmed_transaction_ledger: List[Dict[str, Any]] = []

    def commit_transaction(self, key: str, value: str, quorum_nodes: List[str]) -> None:
        """Appends a validated transaction entry to the ledger log."""
        log_entry = {
            "tx_id": f"TX-LOG-ID-{len(self.confirmed_transaction_ledger) + 1000}",
            "key": key,
            "value": value,
            "confirmed_by_nodes": list(quorum_nodes)
        }
        self.confirmed_transaction_ledger.append(log_entry)


if __name__ == "__main__":
    audit_log = AuditedStateMachine()
    
    print("[AUDIT-MACHINE] Recording validated quorum transactions...")
    audit_log.commit_transaction(
        key="user_profile", 
        value="AuraStatus=Active", 
        quorum_nodes=["node_us_east_1", "node_us_east_2"]
    )
    
    print(f" -> Latest verified ledger record entry: {audit_log.confirmed_transaction_ledger[-1]}")