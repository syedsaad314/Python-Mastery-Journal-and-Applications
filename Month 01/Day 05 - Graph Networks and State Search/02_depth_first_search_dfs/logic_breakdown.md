# Logic Breakdown: Depth-First Search & Stack Traversal
**Engineer:** Syed Saad Bin Irfan

## The Problem
Sometimes the goal isn't finding the shortest path, but rather exhausting all possibilities in a specific branch before moving on. In AI game theory (like Minimax) or deep decision trees, we must simulate a chain of events to its logical conclusion.

## My Approach
I implemented DFS using Python's native recursion stack. Instead of a queue, this uses a LIFO (Last-In-First-Out) mechanism. As it travels down a branch, it adds nodes to the `visited` set to prevent infinite loops in cyclic graphs.

## Critical Thinking
The true advantage here is memory efficiency. BFS must store all nodes at the current depth level in memory, which scales exponentially. DFS only stores the nodes along the current path being explored. When dealing with massive state-spaces (like evaluating a chess board), I will rely on DFS to limit RAM consumption.