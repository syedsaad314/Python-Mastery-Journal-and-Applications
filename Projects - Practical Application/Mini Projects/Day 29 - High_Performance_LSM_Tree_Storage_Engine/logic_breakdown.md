# Portfolio Code Review: Embedded Log-Structured Merge-Tree (LSM-Tree) Storage Engine
**Author:** Syed Saad Bin Irfan

## Practical Context
This integrated storage engine replicates the core architecture used by production log-structured databases (like RocksDB or LevelDB), optimizing write operations while protecting data integrity across crash recovery runs.

## Engineering Standards Applied
* **Atomicity via Pre-Memory Logs:** Appends changes to a persistent transaction log file before updating memory buffers, protecting data from corruption during sudden crashes.
* **Layered Search Routing:** Coordinates data checks through memory tables, Bloom filters, and sparse file indexes sequentially. This pattern drops invalid lookup calls instantly, optimizing read performance.
* **Deterministic Flush Gates:** Implements an automated memory-to-disk conversion pass that structures data into immutable files once capacity limits are hit, maintaining predictable memory footprints.