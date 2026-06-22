# Logic Breakdown: Application Layer Protocol Parsing
**Engineer:** Syed Saad Bin Irfan

## The Problem
Web frameworks automatically extract request endpoints and body content, masking the underlying string parsing logic. We need a clean, protocol-level parser that can break down raw wire-level HTTP strings from scratch.

## My Approach
I implemented an application-layer string evaluation machine based directly on the RFC 7230 specification guidelines. 

The parser breaks down text fields sequentially using the standard network newline separator (`\r\n`). It extracts the request line method and path first, and then maps headers into a key-value structure until it hits an empty line delimiter. Once found, it captures the remaining string data as the payload body, handling the parse cleanly without external regex engines.

## Complexity Profile
* **Runtime Bounds:** Bounded linearly at $O(N)$ relative to the overall byte length of the input packet.
* **Space Constraints:** Scales at $O(N)$ memory space to preserve parsed metadata structures.