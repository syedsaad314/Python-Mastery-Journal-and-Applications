# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Causal Increment Mechanics
Description: Increments a node's local logical counter whenever an internal event 
             or local state mutation takes place.
"""
from typing import Dict

class LocalMutationTracker:
    def __init__(self, current_node: str) -> None:
        self.node_id: str = current_node
        self.clocks: Dict[str, int] = {current_node: 0}

    def register_local_event(self) -> None:
        self.clocks[self.node_id] = self.clocks.get(self.node_id, 0) + 1
        print(f"[MUTATION] Local operation processed on {self.node_id}. Clock map: {self.clocks}")

if __name__ == "__main__":
    tracker = LocalMutationTracker("node_europe")
    tracker.register_local_event()
    tracker.register_local_event()
    assert tracker.clocks["node_europe"] == 2