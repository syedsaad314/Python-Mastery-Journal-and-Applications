# Logic Breakdown: Low-Level Async Raw HTTP Transport Engine
**Engineer:** Syed Saad Bin Irfan

## The Problem
High-level HTTP libraries hide the underlying mechanics of network streams. To build highly optimized custom application protocols, we need to know how to interact directly with raw network byte sequences.

## My Approach
I used `asyncio.open_connection` to open a raw TCP streaming socket directly to port 80 of a target domain. 

I manually formatted an RFC-compliant `GET` request string, converted it to bytes using UTF-8 encoding, and pushed it down the stream. By using `await reader.readline()`, I read the response byte array up to the first newline character, capturing the raw server handshake response directly.

## Complexity Profile
* **Runtime Bounds:** Network speed dependent; network transport handshakes execute in $O(1)$ stream lookups.
* **Space Constraints:** Minimal $O(W)$ memory footprint relative to the length of the string buffer returned by the socket.