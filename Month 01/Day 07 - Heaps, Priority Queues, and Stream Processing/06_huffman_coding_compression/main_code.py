"""
Core Topic: Huffman Coding Text Compression
Description: Building priority allocation prefix code maps using custom tree node tracking.
Lead Engineer: Syed Saad Bin Irfan
GitHub: https://github.com/syedsaad314
LinkedIn: https://www.linkedin.com/in/syed-saad-bin-irfan
"""

import heapq
from collections import Counter

class HuffmanNode:
    def __init__(self, character: str, frequency: int):
        self.character = character
        self.frequency = frequency
        self.left = None
        self.right = None

    # Implement comparison operators to support binary min-heap array ordering
    def __lt__(self, other): return self.frequency < other.frequency

class DataCompressionEngine:
    def __init__(self):
        self.encoding_map = {}

    def _generate_prefix_codes(self, root_node: HuffmanNode, path_string: str) -> None:
        """Recursively traverses the tree to build unique binary prefix codes for each character."""
        if not root_node:
            return
        if root_node.character is not None:
            self.encoding_map[root_node.character] = path_string
            return
            
        self._generate_prefix_codes(root_node.left, path_string + "0")
        self._generate_prefix_codes(root_node.right, path_string + "1")

    def build_compression_tree(self, text: str) -> dict:
        """Constructs the optimal binary prefix-free tree and returns the resulting token code map."""
        if not text: return {}
        frequencies = Counter(text)
        heap = [HuffmanNode(char, freq) for char, freq in frequencies.items()]
        heapq.heapify(heap)

        # Pull the two lowest frequencies, combine them, and re-insert into the heap
        while len(heap) > 1:
            node_left = heapq.heappop(heap)
            node_right = heapq.heappop(heap)
            
            parent_node = HuffmanNode(None, node_left.frequency + node_right.frequency)
            parent_node.left = node_left
            parent_node.right = node_right
            heapq.heappush(heap, parent_node)

        final_root = heap[0] if heap else None
        self._generate_prefix_codes(final_root, "")
        return self.encoding_map

if __name__ == "__main__":
    pipeline = DataCompressionEngine()
    source_corpus = "lossless_compression_data_stream"
    
    code_schema = pipeline.build_compression_tree(source_corpus)
    print(f"Generated Binary Huffman Bit-Mapping Schema: {code_schema}")
    
    bit_sequence = "".join(code_schema[char] for char in source_corpus)
    print(f"Resulting Output Compression Stream Sequence: {bit_sequence}")