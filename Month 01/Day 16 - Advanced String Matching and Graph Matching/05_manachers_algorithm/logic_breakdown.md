# Logic Breakdown: Palindromic Extraction (Manacher's Algorithm)
**Engineer:** Syed Saad Bin Irfan

## The Problem
A standard palindrome search expands outward around each potential center point, which takes $O(N^2)$ time. Additionally, handling even-length palindromes (like `abba`) and odd-length palindromes (like `aba`) separately requires extra case logic.

## My Approach
I implemented **Manacher's Algorithm** to solve both issues:

1. **String Normalization:** The input text is padded with delimiter characters (e.g., `#`). This transforms all even-length palindromes into odd-length structures, allowing a single uniform expansion rule to handle all cases.
2. **Mirror Optimization:** The engine tracks a running palindrome's `center` and its furthest `right boundary`. When evaluating a new position, it looks up its symmetric **mirror position** across the center. It uses the precalculated radius of that mirror to skip redundant character matches, expanding only when a palindrome extends past the known right boundary.

## Complexity Evaluation
* **Processing Runtime:** Pure linear $O(N)$ execution flow.
* **Space Requirements:** $O(N)$ memory footprint to house the padded string variant.