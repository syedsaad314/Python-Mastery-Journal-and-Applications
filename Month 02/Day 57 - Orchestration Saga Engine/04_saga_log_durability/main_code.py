# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Write-Ahead Saga Log Durability
Description: Implements persistent state logging for the saga coordinator, 
             ensuring transactions can pick up where they left off after a crash.
"""
import json
from typing import Dict, Any, List

class DurableSagaLogJournal:
    def __init__(self) -> None:
        self.durable_records: List[str] = []

    def record_transition(self, saga_id: str, current_step: str, targeted_state: str) -> None:
        log_entry = {
            "saga_id": saga_id,
            "step": current_step,
            "state": targeted_state
        }
        # Serialize the entry to simulate writing to a persistent disk
        self.durable_records.append(json.dumps(log_entry))

    def fetch_latest_state(self) -> Dict[str, Any]:
        if not self.durable_records:
            return {}
        return json.loads(self.durable_records[-1])

if __name__ == "__main__":
    journal = DurableSagaLogJournal()
    journal.record_transition("saga_abc", "payment_settle", "COMPENSATING")
    
    latest = journal.fetch_latest_state()
    assert latest["saga_id"] == "saga_abc"
    assert latest["state"] == "COMPENSATING"