# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Concurrent Conflict Detection
Description: Analyzes two vector maps to determine if they are concurrent, 
             indicating a distributed conflict that requires branching versions.
"""
from typing import Dict

class ConflictDetector:
    @staticmethod
    def check_for_concurrency(clock_a: Dict[str, int], clock_b: Dict[str, int]) -> bool:
        # Two clocks are concurrent if neither is causally older than the other
        all_keys = set(clock_a.keys()).union(clock_b.keys())
        a_has_greater = False
        b_has_greater = False
        
        for key in all_keys:
            val_a = clock_a.get(key, 0)
            val_b = clock_b.get(key, 0)
            if val_a > val_b:
                a_has_greater = True
            if val_b > val_a:
                b_has_greater = True
                
        return a_has_greater and b_has_greater

if __name__ == "__main__":
    detector = ConflictDetector()
    # Concurrency Example: node_A advanced separately from node_B
    clock_x = {"node_A": 2, "node_B": 1}
    clock_y = {"node_A": 1, "node_B": 2}
    assert detector.check_for_concurrency(clock_x, clock_y) == True
    print("[DETECTOR] Successfully identified concurrent divergent write paths.")