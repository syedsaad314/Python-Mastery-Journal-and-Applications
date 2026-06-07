"""
Core Topic: Vector Clocks Logical Coordination
Description: Captures partial causal order histories of mutations within distributed systems.
Lead Engineer: Syed Saad Bin Irfan
"""

from typing import Dict, Tuple

class VectorClock:
    """Manages tracking records over isolated process execution timelines without global clock sync."""
    
    def __init__(self, assigned_node_id: str) -> None:
        self.node_id: str = assigned_node_id
        # Internal logical timeline counter map
        self.timestamps_map: Dict[str, int] = {assigned_node_id: 0}

    def increment_local_tick(self) -> None:
        """Increments the local node tick tracker when internal mutations occur."""
        self.timestamps_map[self.node_id] = self.timestamps_map.get(self.node_id, 0) + 1

    def convert_to_payload_snapshot(self) -> Dict[str, int]:
        return dict(self.timestamps_map)

    def merge_incoming_vector_timeline(self, incoming_snapshot: Dict[str, int]) -> None:
        """Merges incoming message timeline matrices to reconcile local state tracking history."""
        # Enforce structural synchronization rules
        for node, incoming_tick in incoming_snapshot.items():
            self.timestamps_map[node] = max(self.timestamps_map.get(node, 0), incoming_tick)
        # Advance the local node tracking clock register to record the merge operation
        self.increment_local_tick()

    @staticmethod
    def compare_causality(clock_a: Dict[str, int], clock_b: Dict[str, int]) -> str:
        """
        Evaluates two logical clock timelines to determine their execution causal relation sequence.
        Returns: 'CAUSALLY_BEFORE', 'CAUSALLY_AFTER', or 'CONCURRENT_CONFLICT'
        """
        all_nodes = set(clock_a.keys()).union(set(clock_b.keys()))
        
        a_has_less_or_equal = False
        b_has_less_or_equal = False
        
        for node in all_nodes:
            tick_a = clock_a.get(node, 0)
            tick_b = clock_b.get(node, 0)
            
            if tick_a < tick_b:
                a_has_less_or_equal = True
            elif tick_a > tick_b:
                b_has_less_or_equal = True

        if a_has_less_or_equal and not b_has_less_or_equal:
            return "CAUSALLY_BEFORE"
        elif b_has_less_or_equal and not a_has_less_or_equal:
            return "CAUSALLY_AFTER"
        return "CONCURRENT_CONFLICT"


if __name__ == "__main__":
    print("[VECTOR-CLOCK] Simulating distributed chronological transactions...")
    
    node_alpha = VectorClock("NODE_ALPHA")
    node_beta = VectorClock("NODE_BETA")

    node_alpha.increment_local_tick()
    tx_snapshot_1 = node_alpha.convert_to_payload_snapshot()

    node_beta.merge_incoming_vector_timeline(tx_snapshot_1)
    tx_snapshot_2 = node_beta.convert_to_payload_snapshot()

    relation = VectorClock.compare_causality(tx_snapshot_1, tx_snapshot_2)
    print(f"[VECTOR-CLOCK] Causal structural analysis result sequence: {relation}")