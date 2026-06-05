# Portfolio Code Review: High-Performance Binary Time-Series Datastore
**Author:** Syed Saad Bin Irfan

## Practical Context
This binary storage utility replicates the low-level data management patterns found inside custom time-series databases (like InfluxDB or Prometheus), compressing application metric tracking points down to dense, highly aligned data sequences.

## Engineering Standards Applied
* **Fixed Structural Packing Optimization:** Packs data snapshots into a minimal 20-byte payload layout (`!QIff`). This approach avoids heavy text formatting overhead, achieving significant space savings compared to standard JSON layouts.
* **Zero-Allocation Buffer Slicing:** Uses a native `memoryview` layout layer combined with `struct.unpack_from` to read file data. This lets the engine extract metrics directly from offset coordinates without allocating temporary sub-array variables.
* **Memory Footprint Caps via Slots:** Employs the `__slots__` compiler optimization directive on data classes. This cuts out individual object instance dictionary mappings, keeping memory flat and predictable during large-scale database operations.