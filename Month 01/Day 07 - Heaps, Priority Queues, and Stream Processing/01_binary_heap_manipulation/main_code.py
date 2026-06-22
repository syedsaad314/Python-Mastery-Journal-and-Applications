"""
Core Topic: Custom Binary Min-Heap Array Implementation
Description: Building structural node transformations with array element indexing arithmetic.
Lead Engineer: Syed Saad Bin Irfan
GitHub: https://github.com/syedsaad314
LinkedIn: https://www.linkedin.com/in/syed-saad-bin-irfan
"""

class CustomMinHeap:
    def __init__(self):
        self.heap = []

    def _get_parent_idx(self, i: int) -> int: return (i - 1) // 2
    def _get_left_child_idx(self, i: int) -> int: return (2 * i) + 1
    def _get_right_child_idx(self, i: int) -> int: return (2 * i) + 2

    def insert(self, value: int) -> None:
        """Appends value to the end and bubbles it up to preserve heap property constraints."""
        self.heap.append(value)
        self._heapify_up(len(self.heap) - 1)

    def extract_min(self) -> int:
        """Removes the absolute minimum root element and trickles the new root down."""
        if not self.heap:
            return None
        if len(self.heap) == 1:
            return self.heap.pop()
            
        min_val = self.heap[0]
        self.heap[0] = self.heap.pop()  # Move the terminal item to root positions
        self._heapify_down(0)
        return min_val

    def _heapify_up(self, index: int) -> None:
        """Restores structural order upward toward the root index."""
        parent = self._get_parent_idx(index)
        if index > 0 and self.heap[index] < self.heap[parent]:
            self.heap[index], self.heap[parent] = self.heap[parent], self.heap[index]
            self._heapify_up(parent)

    def _heapify_down(self, index: int) -> None:
        """Restores structural order downward toward the leaves."""
        smallest = index
        left = self._get_left_child_idx(index)
        right = self._get_right_child_idx(index)
        limit = len(self.heap)

        if left < limit and self.heap[left] < self.heap[smallest]:
            smallest = left
        if right < limit and self.heap[right] < self.heap[smallest]:
            smallest = right

        if smallest != index:
            self.heap[index], self.heap[smallest] = self.heap[smallest], self.heap[index]
            self._heapify_down(smallest)

if __name__ == "__main__":
    engine = CustomMinHeap()
    for metric in [45, 12, 8, 31, 19]:
        engine.insert(metric)
        
    print(f"Internal Balanced Array Layout Vector: {engine.heap}")
    print(f"Extracted Peak Root Priority Member: {engine.extract_min()}")
    print(f"Post-Extraction Array Structural Vector: {engine.heap}")