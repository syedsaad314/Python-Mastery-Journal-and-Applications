"""
Core Topic: Memory Footprint Evaluation
Description: Analyzes object bytes usage directly using the native sys module.
Lead Engineer: Syed Saad Bin Irfan
"""

import sys
from typing import List, Dict, Set

def evaluate_container_footprints() -> None:
    """Evaluates raw memory allocation footprints across various standard collection types."""
    element_limit = 10000
    
    # Generate identical collections to compare underlying structural memory patterns
    raw_list: List[int] = list(range(element_limit))
    raw_set: Set[int] = set(range(element_limit))
    raw_dict: Dict[int, int] = {i: i for i in range(element_limit)}
    
    print("=" * 60)
    print(f" CONTAINER MEMORY FOOTPRINT MATRIX FOR {element_limit} INTERGERS")
    print("=" * 60)
    print(f" List Container Storage Cost : {sys.getsizeof(raw_list):>8} Bytes")
    print(f" Set Container Storage Cost  : {sys.getsizeof(raw_set):>8} Bytes")
    print(f" Dict Container Storage Cost : {sys.getsizeof(raw_dict):>8} Bytes")
    print("=" * 60)

if __name__ == "__main__":
    evaluate_container_footprints()