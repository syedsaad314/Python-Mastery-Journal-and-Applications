# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Distributed Idempotent Consumer Guards
Description: Prevents duplicate event processing anomalies by tracking message identifiers 
             in an isolation filter.
"""
from typing import Set

class IdempotentEventConsumer:
    def __init__(self) -> None:
        self._deduplication_store: Set[str] = set()

    def consume_event(self, message_id: str, business_logic_callback: callable) -> bool:
        if message_id in self._deduplication_store:
            print(f"[DUPLICATE BLOCKED] Event ID '{message_id}' already processed. Safely ignoring.")
            return False
            
        business_logic_callback()
        self._deduplication_store.add(message_id)
        return True

if __name__ == "__main__":
    consumer = IdempotentEventConsumer()
    counter = 0
    
    def increment() -> None:
        global counter
        counter += 1

    r1 = consumer.consume_event("evt_token_99", increment)
    r2 = consumer.consume_event("evt_token_99", increment)
    
    assert r1 is True
    assert r2 is False
    assert counter == 1