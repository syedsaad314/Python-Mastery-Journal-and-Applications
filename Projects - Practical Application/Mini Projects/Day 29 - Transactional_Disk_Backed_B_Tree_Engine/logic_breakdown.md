# Portfolio Code Review: Transactional Disk-Backed Page-Indexed B-Tree Core Engine
**Author:** Syed Saad Bin Irfan

## Practical Context
This database core implements the low-level disk-backed page tree layout used by relational database systems (like PostgreSQL or InnoDB), providing reliable, logarithmic-cost data indexes for large datasets.

## Engineering Standards Applied
* **Explicit File Segment Allocation:** Coordinates block locations using explicit byte offsets, bypassing high-overhead variable serialization wrappers.
* **Hardware-Aligned Binary Formats:** Serializes node properties directly into fixed-size 8-byte configurations using strict binary signatures (`!Q`), matching standard low-level system communication formats.
* **Forced Hardware Data Syncs:** Invokes `os.fsync()` systematically during disk writes. This forces changes past volatile system buffers and down to physical disk surfaces, providing strong crash recovery guarantees.