"""
Core Topic: Idempotent Producer Write Deduplication
Description: Filters out duplicate messages sent by producers due to transient network retries.
Lead Engineer: Syed Saad Bin Irfan
"""

from typing import Dict, Set

class IdempotentProducerFilter:
    """Deduplicates incoming messages using tracking sequence numbers per producer."""
    
    def __init__(self) -> None:
        # Maps producer_id to the last processed message sequence number
        self.producer_sequence_registry: Dict[str, int] = {}

    def validate_and_process(self, producer_id: str, sequence_num: int, payload: str) -> bool:
        """Evaluates sequence numbers, rejecting duplicate items sent during network retries."""
        last_seq = self.producer_sequence_registry.get(producer_id, -1)

        if sequence_num <= last_seq:
            print(f"[DEDUP-REJECT] Discarding duplicate payload from '{producer_id}' with sequence {sequence_num}.")
            return False

        self.producer_sequence_registry[producer_id] = sequence_num
        print(f"[DEDUP-ACCEPT] Ingested message seq {sequence_num} from '{producer_id}' -> '{payload}'")
        return True


if __name__ == "__main__":
    filter_engine = IdempotentProducerFilter()
    
    # Simulate standard message delivery
    assert filter_engine.validate_and_process("prod-01", 0, "MSG_A") == True
    # Simulate a network timeout retry sending the exact same payload again
    assert filter_engine.validate_and_process("prod-01", 0, "MSG_A") == False
    # Process subsequent message sequentially
    assert filter_engine.validate_and_process("prod-01", 1, "MSG_B") == True