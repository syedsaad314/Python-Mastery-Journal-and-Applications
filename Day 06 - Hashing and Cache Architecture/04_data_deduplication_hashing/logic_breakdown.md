# Logic Breakdown: Content-Based Dataset Deduplication
**Engineer:** Syed Saad Bin Irfan

## The Problem
Scraping raw internet text to train machine learning models pulls in massive amounts of duplicate content, like mirrored articles or boilerplate headers. Feeding these duplicates into a model wastes training cycles and causes the model to overfit on repetitive phrases. Performing raw character comparisons across millions of rows scales at an unusable quadratic runtime ($O(N^2)$).

## My Approach
I set up a content-hashed deduplication pipeline. Instead of running expensive string comparisons, I convert each document into a fixed-length signature using the SHA-256 cryptographic algorithm. These signatures are managed inside a hash set, allowing the system to run immediate membership lookups.

## Critical Thinking
*   **Time Complexity:** Hashing scales linearly with document length, $O(M)$. Table lookups execute in absolute constant time, $O(1)$.
*   **Space Complexity:** Memory scales at $O(N)$, storing a 32-byte hash fingerprint for each unique document in the system.

This architecture is essential for cleaning large datasets before training NLP models, keeping training files compact, fast to process, and free of duplicate bias.