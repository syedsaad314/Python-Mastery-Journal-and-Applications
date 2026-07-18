# Lead Engineer: Syed Saad Bin Irfan
"""
Portfolio Layer: CQRS Read-Optimized Data Materialization System
"""
from typing import Dict
from models import TransactionDomainEvent

class MaterializedAccountViewProjection:
    def __init__(self) -> None:
        self.dashboard_index: Dict[str, dict] = {}

    def consume(self, event: TransactionDomainEvent) -> None:
        aid = event.aggregate_id
        etype = event.event_type
        payload = event.payload

        if etype == "LEDGER_OPENED":
            self.dashboard_index[aid] = {
                "account_id": aid,
                "owner_name": payload["owner"],
                "liquid_balance": payload["initial_deposit"],
                "total_transactions": 1,
                "active_status": "ACTIVE"
            }
        elif etype == "FUNDS_CREDITED":
            if aid in self.dashboard_index:
                self.dashboard_index[aid]["liquid_balance"] += payload["amount"]
                self.dashboard_index[aid]["total_transactions"] += 1
        elif etype == "FUNDS_DEBITED":
            if aid in self.dashboard_index:
                self.dashboard_index[aid]["liquid_balance"] -= payload["amount"]
                self.dashboard_index[aid]["total_transactions"] += 1