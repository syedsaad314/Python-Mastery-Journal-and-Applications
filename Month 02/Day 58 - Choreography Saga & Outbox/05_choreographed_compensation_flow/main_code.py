# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Choreographed Compensation Flows
Description: Implements decentralized compensation logic where services watch for 
             failure signals and automatically trigger rollbacks.
"""
from typing import Dict, Any

class ChoreographedInventoryService:
    def __init__(self) -> None:
        self.allocations: Dict[str, str] = {"TX_77": "RESERVED"}
        self.compensation_log: list[str] = []

    def handle_billing_failed_event(self, event_data: Dict[str, Any]) -> None:
        correlation_id = event_data.get("correlation_id")
        if correlation_id in self.allocations:
            # Shift state internally to release held resources
            self.allocations[correlation_id] = "RELEASED_COMPENSATION"
            self.compensation_log.append(f"COMPENSATE:{correlation_id}")

if __name__ == "__main__":
    service = ChoreographedInventoryService()
    failure_signal = {"event_type": "BILLING_FAILED", "correlation_id": "TX_77"}
    
    service.handle_billing_failed_event(failure_signal)
    assert service.allocations["TX_77"] == "RELEASED_COMPENSATION"
    assert service.compensation_log == ["COMPENSATE:TX_77"]