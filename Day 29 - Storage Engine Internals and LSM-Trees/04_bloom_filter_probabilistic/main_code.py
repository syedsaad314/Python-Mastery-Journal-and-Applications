"""
Core Topic: Probabilistic Bloom Filters
Description: Implements a fast bitwise filter to intercept and drop invalid disk query requests instantly.
Lead Engineer: Syed Saad Bin Irfan
"""

import math
from typing import List

class ProbabilisticBloomFilter:
    """Bitmask array that catches missing keys instantly to avoid expensive disk lookups."""
    
    def __init__(self, expected_elements_count: int = 100, false_positive_rate: float = 0.05) -> None:
        # Calculate optimal bit array length and hash function count configurations mathematically
        self.bit_size = int(- (expected_elements_count * math.log(false_positive_rate)) / (math.log(2) ** 2))
        self.hash_count = int((self.bit_size / expected_elements_count) * math.log(2))
        
        # Initialize an empty bitmask array using a pre-allocated bytearray
        self.bit_array = bytearray((self.bit_size + 7) // 8)
        print(f"[BLOOM-CORE] Allocated bit array size: {self.bit_size} bits | Hash functions count: {self.hash_count}")

    def _compute_hash_coordinates(self, input_string: str) -> List[int]:
        """Generates distinct bit coordinates across the array using salt strings."""
        coordinates: List[int] = []
        for i in range(self.hash_count):
            salt_string = f"salt_seed_{i}_{input_string}"
            # Standard FNV-1a non-cryptographic high-speed hashing logic replication
            hash_val = 2166136261
            for char in salt_string:
                hash_val ^= ord(char)
                hash_val = (hash_val * 16777619) & 0xFFFFFFFF
            coordinates.append(hash_val % self.bit_size)
        return coordinates

    def add_key(self, key_string: str) -> None:
        """Sets the calculated bit flag markers to high across the filter array."""
        for position in self._compute_hash_coordinates(key_string):
            byte_index = position // 8
            bit_offset = position % 8
            # Flip the target bit high using bitwise OR operations
            self.bit_array[byte_index] |= (1 << bit_offset)

    def contains_key(self, key_string: str) -> bool:
        """Verifies if a key might exist. Returns False if the key is definitely missing."""
        for position in self._compute_hash_coordinates(key_string):
            byte_index = position // 8
            bit_offset = position % 8
            # Verify if the target bit flag matches high
            if not (self.bit_array[byte_index] & (1 << bit_offset)):
                return False # Key is definitely missing from storage matrices
        return True # Key might be present inside database partitions


if __name__ == "__main__":
    filter_gate = ProbabilisticBloomFilter(expected_elements_count=10, false_positive_rate=0.1)
    
    filter_gate.add_key("saad_token_99")
    filter_gate.add_key("ubit_data")

    # Positive test pass verification
    print(f"[BLOOM-CORE] Checks 'saad_token_99': {filter_gate.contains_key('saad_token_99')} (Must be True)")
    # Negative test pass verification
    print(f"[BLOOM-CORE] Checks 'missing_key': {filter_gate.contains_key('missing_key')} (Must be False)")