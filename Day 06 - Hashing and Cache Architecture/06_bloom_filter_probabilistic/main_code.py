"""
Core Topic: Probabilistic Space-Optimized Bloom Filter
Description: Using a bit array and multiple salt hashes to verify asset absence with zero false negatives.
Lead Engineer: Syed Saad Bin Irfan
GitHub: https://github.com/syedsaad314
LinkedIn: https://www.linkedin.com/in/syed-saad-bin-irfan
"""

import hashlib

class ProbabilisticBloomFilter:
    def __init__(self, bit_array_size: int = 100, hash_pass_count: int = 3):
        self.bit_array_size = bit_array_size
        self.hash_pass_count = hash_pass_count
        # Initialize a zeroed bit flag list tracking array
        self.bit_array = [0] * self.bit_array_size

    def _fetch_bit_indices(self, key: str) -> list[int]:
        """Calculates multiple distinct target bit array indices using salted hashing passes."""
        target_indices = []
        for salting_index in range(self.hash_pass_count):
            salted_string = f"{key}-salt-{salting_index}"
            hash_bytes = hashlib.md5(salted_string.encode('utf-8')).digest()
            position = int.from_bytes(hash_bytes[:4], byteorder='big') % self.bit_array_size
            target_indices.append(position)
        return target_indices

    def insert(self, key: str) -> None:
        """Sets the calculated hash bits to 1, logging the item into the filter."""
        for index in self._fetch_bit_indices(key):
            self.bit_array[index] = 1

    def contains(self, key: str) -> bool:
        """
        Checks if an element is in the filter. 
        Returns False if definitely absent, True if it might be present.
        """
        for index in self._fetch_bit_indices(key):
            if self.bit_array[index] == 0:
                return False  # Guaranteed absolute non-membership match
        return True  # High probability match, could be a false positive due to collision overlaps

if __name__ == "__main__":
    filter_gate = ProbabilisticBloomFilter(bit_array_size=50, hash_pass_count=3)
    
    filter_gate.insert("malicious_domain_entry_1.com")
    filter_gate.insert("malicious_domain_entry_2.com")
    
    print(f"Active Internal Bit Array Mapping Map: {filter_gate.bit_array}")
    print(f"Query Domain 1 (Registered): {filter_gate.contains('malicious_domain_entry_1.com')}")
    print(f"Query Domain 3 (Unregistered): {filter_gate.contains('trusted_secure_platform.org')}")