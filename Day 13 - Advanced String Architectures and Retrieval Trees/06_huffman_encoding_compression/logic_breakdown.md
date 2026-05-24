# Logic Breakdown: Huffman Lossless Encoding Mechanics
**Engineer:** Syed Saad Bin Irfan

## The Problem
Standard text storage uses fixed-length character codes (like 8-bit ASCII), which assigns the exact same memory footprint to every single character. In large text data pipelines, this uniform sizing wastes substantial storage space on frequently used letters.

## My Approach
I implemented a **Huffman Compression Encoder** that uses a greedy frequency optimization model.

1. **Frequency Tracking:** The engine counts the occurrences of each character in the source text.
2. **Min-Heap Tree Assembly:** These frequencies are built into a binary tree from the bottom up using a priority queue (`heapq`). The most frequent characters are pulled up closer to the root of the tree.
3. **Variable-Length Bit Mapping:** Navigating left down a branch adds a `0` to the code, while navigating right adds a `1`. 

This maps high-frequency characters to short bit sequences and rare characters to longer ones, ensuring no generated code acts as a prefix for another (Prefix Rule).

## Operational Metrics
* **Time Complexity:** Tree generation runs in $O(N \log N)$ time, where $N$ is the count of unique symbols.
* **Space Complexity:** Bounded efficiently at $O(N)$ memory allocations to track structural nodes and binary representations.