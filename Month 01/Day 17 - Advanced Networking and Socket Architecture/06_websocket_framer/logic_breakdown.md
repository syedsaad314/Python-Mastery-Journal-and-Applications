# Logic Breakdown: WebSocket Binary Framing
**Engineer:** Syed Saad Bin Irfan

## The Problem
Unlike standard HTTP text blocks, the WebSocket protocol relies on structured binary framing to minimize network overhead. This requires processing data at the bit level to handle masks and lengths correctly.

## My Approach
I built a frame decoding engine based directly on the **RFC 6455 WebSocket specification**.

The script applies bitwise AND operations (`& 0x0F` and `& 0x7F`) to extract specific control flags and payload sizes directly from raw bytes. It isolates the 4-byte masking key sent by the client, then applies a cyclic XOR operation (`^`) across the remaining payload data to decode the client's binary message back into standard text.

## Complexity Profile
* **Runtime Bounds:** Runs in linear time $O(P)$ proportional to the total payload byte length.
* **Space Constraints:** Bounded at $O(P)$ space to assemble the output text string characters.