"""
CORE CONCEPT: Array-Backed Binary Min-Heap Architecture
Implementing a complete priority queue engine from scratch. Elements are structured 
inside a contiguous list, using mathematical pointer transformations to navigate 
parent and child nodes while maintaining tree balance.
"""

class BinaryMinHeap:
    def __init__(self):
        self.heap = []

    def _get_parent_idx(self, idx: int) -> int: return (idx - 1) // 2
    def _get_left_child_idx(self, idx: int) -> int: return (2 * idx) + 1
    def _get_right_child_idx(self, idx: int) -> int: return (2 * idx) + 2

    def push(self, element: float) -> None:
        """Appends an element to the heap, then sifts it upward to restore balance."""
        self.heap.append(element)
        self._sift_up(len(self.heap) - 1)

    def pop(self) -> float:
        """Removes and returns the minimum element, restructuring the heap to rebalance."""
        if not self.heap:
            raise IndexError("Cannot execute pop operations on empty structures.")
        if len(self.heap) == 1:
            return self.heap.pop()
            
        root_value = self.heap[0]
        self.heap[0] = self.heap.pop()  # Move the last element to the root position
        self._sift_down(0)
        
        return root_value

    def _sift_up(self, idx: int) -> None:
        """Balances the heap by swapping a node with its parent if it is smaller."""
        parent = self._get_parent_idx(idx)
        while idx > 0 and self.heap[idx] < self.heap[parent]:
            self.heap[idx], self.heap[parent] = self.heap[parent], self.heap[idx]
            idx = parent
            parent = self._get_parent_idx(idx)

    def _sift_down(self, idx: int) -> None:
        """Balances the heap by swapping a node downward with its smallest child."""
        num_elements = len(self.heap)
        smallest = idx
        
        while True:
            left = self._get_left_child_idx(idx)
            right = self._get_right_child_idx(idx)
            
            if left < num_elements and self.heap[left] < self.heap[smallest]:
                smallest = left
            if right < num_elements and self.heap[right] < self.heap[smallest]:
                smallest = right
                
            if smallest == idx:
                break
                
            self.heap[idx], self.heap[smallest] = self.heap[smallest], self.heap[idx]
            idx = smallest


if __name__ == "__main__":
    pq = BinaryMinHeap()
    for cost in [45.1, 12.3, 89.4, 5.5, 67.2]:
        pq.push(cost)
        
    print(f"Extracted Top Priority Item: {pq.pop()}")
    print(f"Extracted Next Priority Item: {pq.pop()}")