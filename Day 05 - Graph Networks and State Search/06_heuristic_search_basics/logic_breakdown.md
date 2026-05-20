# Logic Breakdown: Greedy Best-First Search & Heuristics
**Engineer:** Syed Saad Bin Irfan

## The Problem
Standard graph searches (BFS/DFS) are "blind". They explore indiscriminately. In massive AI state spaces, I cannot afford to evaluate every node. I need the algorithm to make educated guesses to prune the search tree.

## My Approach
I modified the priority queue system. Instead of prioritizing based on accumulated cost from the start (like Dijkstra), Greedy Best-First Search prioritizes based strictly on a *heuristic*—an estimated remaining distance to the target. It boldly steps toward whatever node "looks" closest.

## Critical Thinking
While Greedy Search is incredibly fast, I acknowledge it doesn't guarantee the mathematically shortest path because it ignores the cost of the path taken so far. However, understanding this failure mode is critical. It perfectly sets up the architecture for A* Search (which combines the accumulated cost of Dijkstra with the heuristic speed of Greedy). This forms the exact basis of spatial AI pathfinding.