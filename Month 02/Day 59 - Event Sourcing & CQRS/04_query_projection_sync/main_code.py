# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Query Projection Sync Channel
Description: Automatically consumes append events to populate read-only, 
             highly optimized query indexes.
"""
from typing import Dict

class AccountReadProjection:
    def __init__(self) -> None:
        # Optimized lookup index tailored for rapid front-end presentation reads
        self.read_database: Dict[str, dict] = {}

    def project_incoming_event(self, aggregate_id: str, event_type: str, payload: dict) -> None:
        if event_type == "ACCOUNT_OPENED":
            self.read_database[aggregate_id] = {
                "owner": payload["holder"],
                "net_worth": payload["initial"],
                "transaction_count": 1
            }
        elif event_type == "FUNDS_DEPOSITED":
            if aggregate_id in self.read_database:
                self.read_database[aggregate_id]["net_worth"] += payload["amount"]
                self.read_database[aggregate_id]["transaction_count"] += 1

if __name__ == "__main__":
    projection = AccountReadProjection()
    projection.project_incoming_event("acc_01", "ACCOUNT_OPENED", {"holder": "Saad", "initial": 1000})
    projection.project_incoming_event("acc_01", "FUNDS_DEPOSITED", {"amount": 500})
    
    view = projection.read_database["acc_01"]
    assert view["net_worth"] == 1500
    assert view["transaction_count"] == 2
    print(f"[PROJECTION SYNCED] Read-optimized model updated: {view}")