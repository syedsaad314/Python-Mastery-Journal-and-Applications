# Logic Breakdown: Hierarchical Inheritance LCA Solvers
**Engineer:** Syed Saad Bin Irfan

## The Problem
In complex directory schemas, user permission hierarchies, or code dependency trees, you frequently need to find the closest shared parent node between two items. For instance, determining the lowest shared folder helps identify where access permissions are inherited, avoiding the performance drain of scanning the entire tree from the root down.

## My Approach
I built a bottom-up **Lowest Common Ancestor (LCA)** resolver. The algorithm searches down the tree using post-order recursion. When a branch encounters one of our target nodes, it bubbles that reference back up. If a parent node receives valid signals from both its left and right subtrees, it confirms that the targets sit on opposite sides of its branch, marking it as the lowest shared junction.

## Critical Thinking
*   **Time Complexity:** Scaled linearly at $O(N)$ in the worst-case scenario, as it may need to evaluate all nodes in an unbalanced tree.
*   **Space Complexity:** Consumes up to $O(H)$ space, tracking recursive memory stack depths relative to tree height ($H$).

This pattern is a staple for resolving style overrides in UI layout trees and managing inherited access control entries across enterprise folder frameworks.