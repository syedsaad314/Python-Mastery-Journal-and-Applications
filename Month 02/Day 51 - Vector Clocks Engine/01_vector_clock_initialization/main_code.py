# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Vector Clock Initialization
Description: Instantiates a basic vector clock state component using dictionary mapping 
             to represent node timelines across isolated networks.
"""
from typing import Dict

class VectorClockCore:
    def __init__(self, system_identity: str) -> None:
        self.owner: str = system_identity
        self.clock_map: Dict[str, int] = {system_identity: 0}

    def fetch_state(self) -> Dict[str, int]:
        return self.clock_map.copy()

if __name__ == "__main__":
    vc = VectorClockCore("node_asia")
    state = vc.fetch_state()
    assert state["node_asia"] == 0
    print(f"[VC-INIT] Successfully tracked empty vector map for local instance: {state}")