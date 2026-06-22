# Logic Breakdown: Variable-Length Quantity Encoding
**Engineer:** Syed Saad Bin Irfan

## The Problem
Allocating a fixed 64-bit memory space (8 bytes) for every single integer in a distributed message payload wastes significant network bandwidth when most transmissions pass small values (like numbers under 100), which could easily fit into a single byte block.

## My Approach
I engineered an efficient unsigned **Varint Codec** utilizing the **Little-Endian Base 128 (LEB128)** protocol pattern, mirroring the compilation models used inside Google Protocol Buffers.

The algorithm breaks numbers down into 7-bit chunks. The 8th bit (the Most Significant Bit, or MSB) serves as a specialized continuation signal flag. If the number requires more bits than the current 7-bit slot allows, the code sets the MSB high (`| 0x80`) and streams subsequent chunks. If the value fits completely, the code clears the bit, automatically flattening low-value tracking metrics down to a single byte footprint.

## Complexity Profile
* **Runtime Bounds:** Logarithmic performance $O(\log_{128} N)$ scaling directly with numerical size parameters.
* **Space Constraints:** Maximizes payload usage allocations, capping storage at a flat 10-byte boundary ceiling for large 64-bit numbers.