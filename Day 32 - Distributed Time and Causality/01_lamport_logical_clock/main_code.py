"""
Core Topic: Lamport Logical Clock
Description: Implements a scalar logical clock tracking partial ordering of events.
Lead Engineer: Syed Saad Bin Irfan
"""

from typing import Tuple, Dict

class LamportClock:
    """Provides monotonically increasing scalar logical timestamps to order distributed events."""
    
    def __init__(self, node_id: str) -> None:
        self.node_id: str = node_id
        self.counter: int = 0

    def tick_internal_event(self) -> int:
        """Increments the clock for a local execution step."""
        self.counter += 1
        return self.counter

    def send_event(self) -> Tuple[int, str]:
        """Increments the clock and produces a payload timestamp to attach to an outgoing message."""
        self.counter += 1
        return (self.counter, self.node_id)

    def receive_event(self, incoming_timestamp: int) -> int:
        """Synchronizes the local clock based on an incoming message timestamp."""
        self.counter = max(self.counter, incoming_timestamp) + 1
        return self.counter


if __name__ == "__main__":
    node_a = LamportClock("node-a")
    node_b = LamportClock("node-b")
    
    # Simulate internal processing on Node A
    node_a.tick_internal_event()
    print(f"[LAMPORT] Node A internal tick. Current value: {node_a.counter}")
    
    # Node A transmits a message to Node B
    tx_timestamp, sender = node_a.send_event()
    print(f"[LAMPORT] Node A dispatched message with timestamp: {tx_timestamp}")
    
    # Node B accepts the message
    node_b.receive_event(tx_timestamp)
    print(f"[LAMPORT] Node B accepted message. Synchronized clock value: {node_b.counter}")