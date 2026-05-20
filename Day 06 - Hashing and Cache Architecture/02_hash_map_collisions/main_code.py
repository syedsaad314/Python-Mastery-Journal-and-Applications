"""
Core Topic: Hash Map Collision Management via Chaining
Description: Building an explicit storage array using modulo math and bucket lists to resolve slot conflicts.
Lead Engineer: Syed Saad Bin Irfan
GitHub: https://github.com/syedsaad314
LinkedIn: https://www.linkedin.com/in/syed-saad-bin-irfan
"""

class CustomHashMap:
    def __init__(self, bucket_count: int = 10):
        self.bucket_count = bucket_count
        # Initialize an array containing isolated list buckets (Chaining mechanism)
        self.table = [[] for _ in range(self.bucket_count)]

    def _generate_hash_index(self, key: str) -> int:
        """Calculates internal array indexing positions via polynomial character folding."""
        hash_value = 0
        for character in str(key):
            hash_value = (hash_value * 31) + ord(character)
        return hash_value % self.bucket_count

    def insert(self, key: str, value: any) -> None:
        """Inserts data pairs into target index paths, updating matching keys on conflict."""
        index = self._generate_hash_index(key)
        bucket = self.table[index]
        
        for i, (existing_key, _) in enumerate(bucket):
            if existing_key == key:
                bucket[i] = (key, value)  # Update in place
                return
        bucket.append((key, value))

    def retrieve(self, key: str) -> any:
        """Searches the assigned collision bucket for a matching data element."""
        index = self._generate_hash_index(key)
        bucket = self.table[index]
        
        for existing_key, value in bucket:
            if existing_key == key:
                return value
        return None

if __name__ == "__main__":
    mapped_storage = CustomHashMap(bucket_count=5)
    
    # Intentionally inserting elements to trigger potential slot index collisions
    mapped_storage.insert("user_id_101", "Syed Saad")
    mapped_storage.insert("user_id_202", "Alex Reynolds")
    mapped_storage.insert("user_id_303", "Maria Gomez")
    
    print(f"Bucket Array Layout Configuration: {mapped_storage.table}")
    print(f"Retrieved Identity Core Check: {mapped_storage.retrieve('user_id_101')}")