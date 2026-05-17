"""
CORE CONCEPT: Monolithic Hash Table with Linear Probing Resolution
Building a foundational key-value store from scratch. Implements an internal fixed array,
a custom string hashing function, and a linear open-addressing system to resolve collisions.
"""

class CustomFixedHashTable:
    def __init__(self, capacity: int = 16):
        self.capacity = capacity
        # Storing buckets as [Key, Value] pairs or None
        self.buckets = [None] * self.capacity
        self.size = 0

    def _generate_hash(self, key: str) -> int:
        """Generates a deterministic hash code using a prime multiplier algorithm."""
        hash_val = 5381
        for char in key:
            hash_val = ((hash_val << 5) + hash_val) + ord(char)
        return hash_val % self.capacity

    def put(self, key: str, value: any) -> None:
        """Inserts or updates a value using linear probing to handle bucket conflicts."""
        if self.size >= self.capacity // 2:
            raise RuntimeError("Hash table structure requires resizing to clear bucket density.")

        index = self._generate_hash(key)
        
        while self.buckets[index] is not None:
            if self.buckets[index][0] == key:
                self.buckets[index][1] = value  # Key update step
                return
            index = (index + 1) % self.capacity  # Linear search step down the line
            
        self.buckets[index] = [key, value]
        self.size += 1

    def get(self, key: str) -> any:
        """Retrieves a mapped value or raises a KeyError if the identifier is missing."""
        index = self._generate_hash(key)
        start_index = index
        
        while self.buckets[index] is not None:
            if self.buckets[index][0] == key:
                return self.buckets[index][1]
            index = (index + 1) % self.capacity
            if index == start_index:
                break
                
        raise KeyError(f"Key mapping '{key}' not found within table buckets.")


if __name__ == "__main__":
    table = CustomFixedHashTable(capacity=8)
    table.put("loss_rate", 0.024)
    table.put("accuracy", 0.981)
    
    print(f"Retrieved loss_rate: {table.get('loss_rate')}")
    print(f"Retrieved accuracy: {table.get('accuracy')}")