# Logic Breakdown: Byte-Pair Encoding (BPE)
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
Word-level tokenization produces massive vocabularies and completely fails on Out-Of-Vocabulary (OOV) words. Character-level tokenization prevents OOV errors but stretches sequence lengths too far, breaking transformer context windows.

## My Approach
I engineered the Byte-Pair Encoding (BPE) compression algorithm. The engine starts by treating every word as a sequence of discrete characters. It statistically tracks all adjacent character pairs. At each iteration, it finds the most frequent pair (e.g., `e` and `s`) and permanently merges them into a new single token (`es`). Iterating this mathematically bridges the gap between characters and words, ensuring common words become single tokens while rare words decompose gracefully into learned subword roots.

## Complexity Profile
* Runtime Bounds: $O(M \cdot V \cdot L)$ where $M$ is merges, $V$ is vocabulary size, and $L$ is max word length.
* Space Constraints: $O(V)$ tracking the vocabulary frequency hash map.