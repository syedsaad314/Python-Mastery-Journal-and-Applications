# Logic Breakdown: Connectionless UDP Broadcast Transmission
**Engineer:** Syed Saad Bin Irfan

## The Problem
TCP requires a formal three-way handshake before transmitting data, which introduces unnecessary overhead for simple tracking signals, such as checking if service nodes are alive across a local network.

## My Approach
I utilized a **UDP Datagram Socket Engine** (`SOCK_DGRAM`). This setup bypasses connection tracking completely. 

By applying the `SO_BROADCAST` socket option directly, the operating system opens up the network stack to transmit un-targeted packets. The target address is set to the absolute broadcast address (`255.255.255.255`), letting any listening interface on that network segment intercept the beacon in a single transmission step.

## Complexity Profile
* **Runtime Bounds:** Strictly $O(1)$ execution performance per packet sent.
* **Space Constraints:** Bounded at $O(1)$ space, as no connection state tracking tables are managed in memory.