"""
Core Topic: Huffman Lossless Compression Mechanics
Description: Generates variable-length bit codes based on character frequency tracking.
Lead Engineer: Syed Saad Bin Irfan
GitHub: https://github.com/syedsaad314
LinkedIn: https://www.linkedin.com/in/syed-saad-bin-irfan
"""

import heapq
from typing import Dict, List, Tuple

class HuffmanNode:
    def __init__(self, char: str, freq: int) -> None:
        self.char: str = char
        self.freq: int = freq
        self.left: 'HuffmanNode' = None
        self.right: 'HuffmanNode' = None

    def __lt__(self, other: 'HuffmanNode') -> bool:
        # Min-Heap sorting evaluation based on node frequencies
        return self.freq < other.freq

class HuffmanEncoder:
    def __init__(self) -> None:
        self.encoding_table: Dict[str, str] = {}

    def _build_codes_recursive(self, node: HuffmanNode, current_bitstring: str) -> None:
        """Traverses the encoding tree to map characters to their new binary prefixes."""
        if not node: return
        
        if node.char is not None:
            self.encoding_table[node.char] = current_bitstring
            return

        self._build_codes_recursive(node.left, current_bitstring + "0")
        self._build_codes_recursive(node.right, current_bitstring + "1")

    def generate_huffman_tree(self, text: str) -> HuffmanNode:
        """Builds an optimized binary compression tree based on character frequencies."""
        frequencies: Dict[str, int] = {}
        for char in text:
            frequencies[char] = frequencies.get(char, 0) + 1

        min_heap: List[HuffmanNode] = [HuffmanNode(c, f) for c, f in frequencies.items()]
        heapq.heapify(min_heap)

        while len(min_heap) > 1:
            left_child = heapq.heappop(min_heap)
            right_child = heapq.heappop(min_heap)

            # Create an intermediate branch node combining the child frequencies
            parent = HuffmanNode(char=None, freq=left_child.freq + right_child.freq)
            parent.left = left_child
            parent.right = right_child
            heapq.heappush(min_heap, parent)

        root = min_heap[0]
        self._build_codes_recursive(root, "")
        return root

    def encode(self, text: str) -> str:
        """Converts raw string characters into an optimized, compressed bit sequence."""
        if not self.encoding_table:
            self.generate_huffman_tree(text)
        return "".join(self.encoding_table[char] for char in text)


if __name__ == "__main__":
    encoder = HuffmanEncoder()
    corpus_data = "BOSRIKAY REPOSITORY DEKH LE AIK DAFA"
    
    compressed_bits = encoder.encode(corpus_data)
    print(f"Original String Length: {len(corpus_data) * 8} raw bits (Standard ASCII)")
    print(f"Compressed Bit Sequence: {compressed_bits}")
    print(f"Compressed Sequence Length: {len(compressed_bits)} bits")
    print("Character Binary Code Map:")
    for symbol, code in encoder.encoding_table.items():
        print(f"  Symbol '{symbol}' ---> Transformed Code: {code}")