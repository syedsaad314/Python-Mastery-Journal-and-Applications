"""
Core Topic: Vector Clocks Concurrency Analyzer
Description: Tracks logical history across multiple processes to detect concurrent conflicts.
Lead Engineer: Syed Saad Bin Irfan
"""

from typing import Dict, Any, Tuple

class VectorClock:
    """Maintains a vector of logical counters to precisely capture causality and concurrency."""
    
    def __init__(self, node_id: str) -> None:
        self.node_id: str = node_id
        # The clock maps node IDs to their last known logical state counters
        self.clock_vector: Dict[str, int] = {node_id: 0}

    def tick_local(self) -> None:
        """Increments the local counter entry within the vector."""
        self.clock_vector[self.node_id] = self.clock_vector.get(self.node_id, 0) + 1

    def generate_message_vector(self) -> Dict[str, int]:
        """Ticks the local clock and returns a copy of the current vector state for transport."""
        self.tick_local()
        return dict(self.clock_vector)

    def merge_incoming(self, incoming_vector: Dict[str, int]) -> None:
        """Merges an incoming vector by taking the maximum value for each node entry."""
        all_keys = set(self.clock_vector.keys()).union(incoming_vector.keys())
        for key in all_keys:
            self.clock_vector[key] = max(self.clock_vector.get(key, 0), incoming_vector.get(key, 0))
        self.tick_local()

    @staticmethod
    def evaluate_causality(v1: Dict[str, int], v2: Dict[str, int]) -> str:
        """
        Compares two vectors to determine their relationship:
        Returns 'V1_ANCESTOR_OF_V2', 'V2_ANCESTOR_OF_V1', or 'CONCURRENT_CONFLICT'.
        """
        all_keys = set(v1.keys()).union(v2.keys())
        v1_dominated = False
        v2_dominated = False
        
        for k in all_keys:
            val1 = v1.get(k, 0)
            val2 = v2.get(k, 0)
            if val1 < val2:
                v1_dominated = True
            if val2 < val1:
                v2_dominated = True
                
        if v1_dominated and not v2_dominated:
            return "V1_ANCESTOR_OF_V2"
        if v2_dominated and not v1_dominated:
            return "V2_ANCESTOR_OF_V1"
        if not v1_dominated and not v2_dominated:
            return "IDENTICAL_STATE"
        return "CONCURRENT_CONFLICT"


if __name__ == "__main__":
    # Setup independent vectors representing distinct version states
    state_alpha = {"node_1": 2, "node_2": 1}
    state_beta  = {"node_1": 1, "node_2": 3}
    state_gamma = {"node_1": 3, "node_2": 1}
    
    print("[VECTOR-CLOCK] Evaluating concurrency profiles between states:")
    print(f" -> Alpha vs Beta:  {VectorClock.evaluate_causality(state_alpha, state_beta)}")
    print(f" -> Alpha vs Gamma: {VectorClock.evaluate_causality(state_alpha, state_gamma)}")