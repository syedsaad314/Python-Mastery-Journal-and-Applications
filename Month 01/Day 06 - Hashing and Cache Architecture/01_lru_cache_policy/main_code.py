"""
Core Topic: Least Recently Used (LRU) Cache Implementation
Description: Fusing a hash table with a doubly linked list to build a cache evictor.
Lead Engineer: Syed Saad Bin Irfan
GitHub: https://github.com/syedsaad314
LinkedIn: https://www.linkedin.com/in/syed-saad-bin-irfan
"""

class Node:
    def __init__(self, key: str, value: any):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.lookup = {}
        
        # Initialize sentinel head and tail nodes to eliminate edge case null checks
        self.head = Node("head", None)
        self.tail = Node("tail", None)
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node: Node) -> None:
        """Detaches an existing node from its current position in the linked list."""
        prev_node = node.prev
        next_node = node.next
        prev_node.next = next_node
        next_node.prev = prev_node

    def _add_to_head(self, node: Node) -> None:
        """Inserts a node immediately after the sentinel head (marking it most recent)."""
        node.next = self.head.next
        node.next.prev = node
        self.head.next = node
        node.prev = self.head

    def get(self, key: str) -> any:
        """Retrieves an item and bumps it to the head of the cache hierarchy."""
        if key in self.lookup:
            node = self.lookup[key]
            self._remove(node)
            self._add_to_head(node)
            return node.value
        return -1

    def put(self, key: str, value: any) -> None:
        """Inserts a new value, evicting the least recently used node if capacity is breached."""
        if key in self.lookup:
            self._remove(self.lookup[key])
            
        new_node = Node(key, value)
        self._add_to_head(new_node)
        self.lookup[key] = new_node
        
        if len(self.lookup) > self.capacity:
            # Evict from the tail of the linked list
            lru_node = self.tail.prev
            self._remove(lru_node)
            del self.lookup[lru_node.key]

if __name__ == "__main__":
    cache = LRUCache(capacity=3)
    cache.put("api_token_1", "authenticated_user_a")
    cache.put("api_token_2", "authenticated_user_b")
    cache.put("api_token_3", "authenticated_user_c")
    
    # Accessing token 1 makes it the most recently used item
    cache.get("api_token_1")
    
    # Inserting a fourth token forces eviction of token 2 (the current oldest item)
    cache.put("api_token_4", "authenticated_user_d")
    
    print(f"Token 1 Value (Active): {cache.get('api_token_1')}")
    print(f"Token 2 Value (Evicted): {cache.get('api_token_2')}")