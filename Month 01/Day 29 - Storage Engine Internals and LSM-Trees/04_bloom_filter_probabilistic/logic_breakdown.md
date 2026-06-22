# Logic Breakdown: Probabilistic Bloom Filters
**Engineer:** Syed Saad Bin Irfan

## The Problem
When looking up missing keys across database partitions, the engine is forced to search through multiple immutable disk files (SSTables) sequentially. This creates unnecessary disk read load that can slow down overall read path operations.

## My Approach
I engineered a space-efficient bitmask helper using a **Probabilistic Bloom Filter** architecture.

The filter maps keys to explicit bit coordinates across a small `bytearray` bitmask using a series of fast, non-cryptographic hashing functions. If any calculated bit position reads low (`0`) during a query check, the engine can confirm instantly that the key is missing from the file. This lets the system bypass expensive, useless disk lookups entirely, ensuring disk operations are focused only on valid data locations.

## Complexity Profile
* **Runtime Bounds:** Adding keys and executing lookup checks run in constant $O(K)$ time (where $K$ matches hash function density limits).
* **Space Constraints:** Uses a highly compressed memory layout, requiring only a few bits of storage per indexed element.