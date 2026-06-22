# Logic Breakdown: Rabin-Karp Rolling Hash Engine
**Engineer:** Syed Saad Bin Irfan

## The Problem
Comparing raw strings character-by-character over and over as you slide across a large text block wastes compute cycles. To scale efficiently, you need a way to verify if a text window matches your pattern in a single, fast operation.

## My Approach
I built a **Rabin-Karp Matching Engine** that uses a **Polynomial Rolling Hash**. 

Instead of comparing raw strings directly, the engine converts the target pattern into a hash value. As it slides across the text, it computes the hash of the current window. 

The key optimization is the rolling hash mechanism: it drops the leading character and adds the trailing character mathematically in **$O(1)$ constant time**.

$$\text{Next Hash} = \left( D \times (\text{Current Hash} - \text{Old Char} \times H) + \text{New Char} \right) \pmod Q$$

If the hash values match, a character-by-character check runs to confirm the match and handle any hash collisions caused by the modulo math.

## Architectural Metrics
* **Time Complexity:** Average case is a highly efficient $O(N + M)$, though it can degrade to $O(N \times M)$ if a poor choice of prime number causes frequent hash collisions.
* **Space Complexity:** $O(1)$ auxiliary memory requirement.