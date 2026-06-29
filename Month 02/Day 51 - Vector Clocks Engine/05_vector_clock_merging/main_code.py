# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Vector Clock Merging
Description: Combines two vector clocks during synchronization, creating a new unified 
             baseline clock that encapsulates the history of both paths.
"""
from typing import Dict

class VectorClockMerger:
    @staticmethod
    def merge_vectors(local_clock: Dict[str, int], incoming_clock: Dict[str, int]) -> Dict[str, int]:
        merged_result: Dict[str, int] = {}
        all_keys = set(local_clock.keys()).union(incoming_clock.keys())
        
        for key in all_keys:
            merged_result[key] = max(local_clock.get(key, 0), incoming_clock.get(key, 0))
            
        return merged_result

if __name__ == "__main__":
    merger = VectorClockMerger()
    v1 = {"node_A": 3, "node_B": 1}
    v2 = {"node_A": 2, "node_B": 4}
    res = merger.merge_vectors(v1, v2)
    assert res == {"node_A": 3, "node_B": 4}