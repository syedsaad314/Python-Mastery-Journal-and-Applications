# Logic Breakdown: DAG Validation & Cycle Detection
**Engineer:** Syed Saad Bin Irfan

## The Problem
In modern Data Engineering, we rely heavily on DAGs (Directed Acyclic Graphs) for orchestrating tools like Apache Airflow. If a data pipeline loops back on itself (Task A -> Task B -> Task A), the system will hang infinitely. I needed a mechanism to structurally validate pipelines before execution.

## My Approach
I built a recursive DFS cycle detector. The key innovation here is maintaining a `recursion_stack` set alongside the standard `visited` set. The `recursion_stack` tracks the *current* active branch. If the algorithm encounters a node that is already in the current recursion stack, it has found a "back-edge"—meaning a cycle exists.

## Critical Thinking
Simply tracking `visited` nodes isn't enough in directed graphs, because branches can safely merge. By strictly tracking the active traversal stack, I can programmatically reject invalid workflow configurations before allocating compute resources to them.