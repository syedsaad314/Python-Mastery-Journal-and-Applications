# Logic Breakdown: Virtual Nodes (VNodes) Distribution
**Engineer:** Syed Saad Bin Irfan

## The Problem
In a basic hash ring, servers can end up clustered close together by chance, creating unbalanced sections on the ring. This leads to data hotspots, where one server handles way more traffic and data than its peers.

## My Approach
I upgraded the ring architecture to use **Virtual Nodes (VNodes)**.

Instead of hashing a server name once, we append a counter to the name (e.g., `server_node_1-vnode-0`, `server_node_1-vnode-1`) and hash it multiple times (e.g., 150 times per server). This distributes virtual points for each physical server evenly across the entire hash ring, smoothing out data distribution and ensuring a balanced workload across the cluster.

## Complexity Profile
* **Runtime Bounds:** Lookups take $O(\log(N \cdot V))$ time, where $V$ is the number of virtual nodes per physical machine. Adding a server takes $O(N \cdot V)$ time to insert the virtual node entries in sorted order.
* **Space Constraints:** Memory usage increases to $O(N \cdot V)$ to map and track all virtual node locations on the ring.