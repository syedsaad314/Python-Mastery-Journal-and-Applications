# Logic Breakdown: PageRank Eigenvector Centrality
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
Counting raw incoming edges (In-Degree) is a poor measure of node importance. A web page with 1 link from Google is vastly more important than a page with 1,000 links from unknown spam sites. We must recursively measure importance based on the importance of the referrers.

## My Approach
I implemented the Google PageRank algorithm via the **Power Iteration Method**. 
Mathematically, finding the steady-state importance is equivalent to finding the principal eigenvector of the graph's modified adjacency matrix. 
I apply the Damping Factor ($d = 0.85$); this simulates a random surfer who clicks links 85% of the time but gets bored and teleports to a random page 15% of the time, solving "spider trap" sink nodes. By iteratively computing $v = \frac{1 - d}{N} + d \cdot M v$, the probability vector inherently converges to the dominant eigenvector in just a few dozen loops.

## Complexity Profile
* Runtime Bounds: $O(I \cdot N^2)$ dense matrix multiplication bounded by $I$ iterations until tolerance threshold.
* Space Constraints: $O(N^2)$ to store the column-stochastic transition matrix layout $M$.