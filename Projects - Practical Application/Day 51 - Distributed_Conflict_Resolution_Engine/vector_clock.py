# Lead Engineer: Syed Saad Bin Irfan
"""
Portfolio Layer: Vector Clock Algebraic Engine
"""
from typing import Dict, Tuple

class VectorClockEngine:
    @staticmethod
    def increment(clock: Dict[str, int], node_id: str) -> Dict[str, int]:
        updated = clock.copy()
        updated[node_id] = updated.get(node_id, 0) + 1
        return updated

    @staticmethod
    def compare_ordering(clock_a: Dict[str, int], clock_b: Dict[str, int]) -> str:
        """
        Determines causal relationships using partial order rules:
        - OLDER: clock_a strictly preceded clock_b
        - NEWER: clock_a strictly succeeded clock_b
        - CONCURRENT: Divergent updates occurred in parallel
        - IDENTICAL: Matching histories
        """
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

        if a_has_greater and b_has_greater:
            return "CONCURRENT"
        if a_has_greater and not b_has_greater:
            return "NEWER"
        if b_has_greater and not a_has_greater:
            return "OLDER"
        return "IDENTICAL"

    @staticmethod
    def merge(clock_a: Dict[str, int], clock_b: Dict[str, int]) -> Dict[str, int]:
        merged: Dict[str, int] = {}
        for k in set(clock_a.keys()).union(clock_b.keys()):
            merged[k] = max(clock_a.get(k, 0), clock_b.get(k, 0))
        return merged