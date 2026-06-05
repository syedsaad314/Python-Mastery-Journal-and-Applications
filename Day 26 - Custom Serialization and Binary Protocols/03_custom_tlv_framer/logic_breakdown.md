# Logic Breakdown: Type-Length-Value Binary Framing Protocol
**Engineer:** Syed Saad Bin Irfan

## The Problem
When parsing a continuous stream of incoming TCP bytes, network packets can easily get clumped together or split into irregular chunks, leading to data framing errors if your application cannot identify packet boundaries accurately.

## My Approach
I engineered a streaming protocol decoder using a strict **Type-Length-Value (TLV)** framing architecture.

The parser reads data frames sequentially using a fixed 3-byte layout configuration header (`!BH`). The network frame type is mapped to a single byte tag, followed by a 2-byte integer defining the explicit length of the variable data payload. This structural layout acts as a protective boundary, letting the decoder calculate packet cut points accurately and process data frames without relying on slow end-of-packet delimiters.

## Complexity Profile
* **Runtime Bounds:** Packs and unpacks data frames in linear $O(N)$ time relative to payload length.
* **Space Constraints:** Linear memory footprint $O(N)$ matching incoming data stream slices.