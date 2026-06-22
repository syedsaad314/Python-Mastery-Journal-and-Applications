# Logical Breakdown: Custom Hash Engine with Linear Probing

### The Problem
Data operations rely heavily on constant-time lookups using key-value dictionaries. Simply relying on built-in types obscures how string inputs map to physical memory buckets and how systems resolve structural address collisions when multiple keys generate identical hashes.

### Architectural Thought Process
I built a fixed-capacity bucket array and paired it with a deterministic hashing algorithm using a prime factor design. When two keys map to the same target index, the linear probing mechanism moves down the array step-by-step to find the next available slot. To prevent infinite loops during lookups, the system restricts insertions past a 50% capacity threshold.

### Complexity & Scope
*   **Time Complexity:** Averages a constant $O(1)$ efficiency for reads and writes, scaling to a linear $O(N)$ if high bucket density triggers consecutive collisions.
*   **AI/ML Real-world Application:** This architecture demonstrates the underlying layout of database indexing systems, caching frameworks, and Python’s internal dictionary type.