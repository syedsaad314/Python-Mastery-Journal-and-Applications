"""
Core Topic: Database LRU Page Cache Buffers
Description: Implements an eviction cache to pin high-frequency data blocks in memory.
Lead Engineer: Syed Saad Bin Irfan
"""

from typing import Dict, Optional

class LRUDoubleLinkedListNode:
    """Represents a structural node inside an LRU double linked list cache."""
    __slots__ = ("key", "value", "prev", "next")
    
    def __init__(self, key_string: str, value_string: str) -> None:
        self.key: str = key_string
        self.value: str = value_string
        self.prev: Optional[LRUDoubleLinkedListNode] = None
        self.next: Optional[LRUDoubleLinkedListNode] = None


class LeastRecentlyUsedPageCache:
    """Cache controller that evicts least-recently-used pages when hitting allocation limits."""
    
    def __init__(self, capacity_slots: int = 3) -> None:
        self.capacity: int = capacity_slots
        self.lookup_map: Dict[str, LRUDoubleLinkedListNode] = {}
        
        # Establish boundary sentinel nodes to ensure fast link adjustments
        self.head = LRUDoubleLinkedListNode("HEAD_SENTINEL", "")
        self.tail = LRUDoubleLinkedListNode("TAIL_SENTINEL", "")
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove_node(self, node: LRUDoubleLinkedListNode) -> None:
        """Detaches a data node from its neighbors inside the linked list."""
        prev_node = node.prev
        next_node = node.next
        if prev_node: prev_node.next = next_node
        if next_node: next_node.prev = prev_node

    def _add_node_to_head_position(self, node: LRUDoubleLinkedListNode) -> None:
        """Inserts a data node directly behind the head sentinel position."""
        node.next = self.head.next
        node.prev = self.head
        
        if self.head.next: self.head.next.prev = node
        self.head.next = node

    def get_cached_page(self, key_string: str) -> Optional[str]:
        """Fetches items from cache, moving the targeted node to the head position."""
        if key_string in self.lookup_map:
            target_node = self.lookup_map[key_string]
            self._remove_node(target_node)
            self._add_node_to_head_position(target_node)
            return target_node.value
        return None

    def pin_page_to_cache(self, key_string: str, value_string: str) -> None:
        """Caches data rows, evicting the oldest page node if capacity limits are breached."""
        if key_string in self.lookup_map:
            existing_node = self.lookup_map[key_string]
            existing_node.value = value_string
            self._remove_node(existing_node)
            self._add_node_to_head_position(existing_node)
            return

        if len(self.lookup_map) >= self.capacity:
            # Evict the oldest node located directly in front of the tail sentinel
            oldest_node = self.tail.prev
            if oldest_node and oldest_node is not self.head:
                print(f"[CACHE] Capacity threshold limit reached. Evicting oldest key: '{oldest_node.key}'")
                self._remove_node(oldest_node)
                del self.lookup_map[oldest_node.key]

        new_node = LRUDoubleLinkedListNode(key_string, value_string)
        self.lookup_map[key_string] = new_node
        self._add_node_to_head_position(new_node)


if __name__ == "__main__":
    print("[CACHE-LRU] Initializing high-frequency page buffer pool...")
    buffer_pool = LeastRecentlyUsedPageCache(capacity_slots=2)

    buffer_pool.pin_page_to_cache("page_idx_1", "binary_sector_a")
    buffer_pool.pin_page_to_cache("page_idx_2", "binary_sector_b")
    
    # Refresh access history to shift page 1 to the head position
    buffer_pool.get_cached_page("page_idx_1")
    
    # This insertion should evict page 2 instead of page 1
    buffer_pool.pin_page_to_cache("page_idx_3", "binary_sector_c")
    print(f"[CACHE-LRU] Verification. Target page_idx_1 status: {buffer_pool.get_cached_page('page_idx_1')}")