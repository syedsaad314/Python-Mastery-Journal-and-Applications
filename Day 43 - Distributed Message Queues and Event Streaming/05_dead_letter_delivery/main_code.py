"""
Core Topic: Poison Pill Poison Pill Sinks (DLQ)
Description: Isolates unparseable or corrupted event payloads into a Dead Letter Queue.
Lead Engineer: Syed Saad Bin Irfan
"""

from typing import List, Dict

class DeadLetterStreamingSink:
    """Routes corrupted or unparseable event payloads into an isolated DLQ stream."""
    
    def __init__(self) -> None:
        self.dlq_ledger: List[Dict[str, any]] = []

    def route_poison_pill(self, raw_data: str, error_reason: str) -> None:
        """Isolates bad payloads to prevent them from blocking the main stream pipelines."""
        poison_record = {
            "raw_payload": raw_data,
            "error_log": error_reason
        }
        self.dlq_ledger.append(poison_record)
        print(f"[DLQ-ROUTING] Isolated corrupt message to DLQ. Reason: {error_reason}")


if __name__ == "__main__":
    dlq = DeadLetterStreamingSink()
    # Simulate parsing structural exceptions from corrupted data input
    dlq.route_poison_pill("{invalid_json_packet", "JSONDecodeError parsing string values.")
    assert len(dlq.dlq_ledger) == 1