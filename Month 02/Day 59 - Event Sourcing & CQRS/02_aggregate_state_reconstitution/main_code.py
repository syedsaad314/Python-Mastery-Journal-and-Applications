# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Aggregate State Reconstitution
Description: Rebuilds an application's current working memory state dynamically 
             by replaying sequential historical event blocks.
"""
from typing import List

class BankAccountAggregate:
    def __init__(self, account_id: str) -> None:
        self.account_id = account_id
        self.balance = 0
        self.status = "NEW"
        self.version = 0

    def apply_event(self, event_type: str, payload: dict) -> None:
        if event_type == "ACCOUNT_OPENED":
            self.balance = payload["initial"]
            self.status = "ACTIVE"
        elif event_type == "FUNDS_DEPOSITED":
            self.balance += payload["amount"]
        elif event_type == "FUNDS_WITHDRAWN":
            self.balance -= payload["amount"]
        self.version += 1

    def reconstitute_from_history(self, history: List[object]) -> None:
        for event in history:
            self.apply_event(event.event_type, event.payload)

if __name__ == "__main__":
    # Mocking historical elements locally
    class MockEvent:
        def __init__(self, etype, payload):
            self.event_type = etype
            self.payload = payload

    history_log = [
        MockEvent("ACCOUNT_OPENED", {"initial": 1000}),
        MockEvent("FUNDS_DEPOSITED", {"amount": 500}),
        MockEvent("FUNDS_WITHDRAWN", {"amount": 200})
    ]
    
    aggregate = BankAccountAggregate("acc_99")
    aggregate.reconstitute_from_history(history_log)
    assert aggregate.balance == 1300
    assert aggregate.version == 3
    print(f"[RECONSTITUTION CONFIRMED] State successfully built from history logs. Current balance: {aggregate.balance}")