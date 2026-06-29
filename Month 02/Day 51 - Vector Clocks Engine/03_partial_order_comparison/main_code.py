# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Partial Order Comparison Operations
Description: Evaluates whether one vector clock causally preceded another, 
             establishing a strict chronological sequence.
"""
from typing import Dict

class CausalOrderEvaluator:
    @staticmethod
    def is_causally_older(clock_a: Dict[str, int], clock_b: Dict[str, int]) -> bool:
        # Returns True if clock_a strictly happened before clock_b
        all_keys = set(clock_a.keys()).union(clock_b.keys())
        at_least_one_strictly_less = False
        
        for key in all_keys:
            val_a = clock_a.get(key, 0)
            val_b = clock_b.get(key, 0)
            if val_a > val_b:
                return False
            if val_a < val_b:
                at_least_one_strictly_less = True
                
        return at_least_one_strictly_less

if __name__ == "__main__":
    c1 = {"node_A": 1, "node_B": 2}
    c2 = {"node_A": 2, "node_B": 2}
    evaluator = CausalOrderEvaluator()
    assert evaluator.is_causally_older(c1, c2) == True
    assert evaluator.is_causally_older(c2, c1) == False