# Logic Breakdown: Levenshtein Edit Distance
**Engineer:** Syed Saad Bin Irfan

## The Problem
Autocorrect features and fuzzy search engines need to know "how close" a typo is to a real word. To do this, we need to mathematically quantify the transformation cost by counting the minimum number of single-character insertions, deletions, or substitutions. 

## My Approach
I implemented the **Levenshtein Matrix**. The engine initializes a 2D grid where the edges represent the cost of reducing a word to an empty string. As the nested loops run, a character match costs nothing (inheriting the diagonal value). A mismatch triggers the core transition rule: the engine looks at the adjacent cells representing insertion (left), deletion (top), and replacement (diagonal), picks the lowest cost among them, and adds $1$ for the current action.

## Critical Thinking
*   **Time Complexity:** Stable $O(M \times N)$ matching grid calculation.
*   **Space Complexity:** $O(M \times N)$ tracking matrix. 

This engine is the backbone of NLP correction pipelines and search query suggestion logic.