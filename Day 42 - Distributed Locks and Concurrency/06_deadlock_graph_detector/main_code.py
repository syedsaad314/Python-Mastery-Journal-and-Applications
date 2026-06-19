"""
Core Topic: Distributed Dependency Deadlock Detection
Description: Uses depth-first cycle detection to identify deadlocks in resource dependency graphs.
Lead Engineer: Syed Saad Bin Irfan
"""

from typing import Dict, List, Set

class DistributedDeadlockGraphDetector:
    """Analyzes resource allocation dependency chains to catch circular deadlocks."""
    
    def __init__(self, dependency_graph: Dict[str, List[str]]) -> None:
        self.graph = dependency_graph

    def contains_circular_deadlock(self) -> bool:
        """Runs a Depth-First Search (DFS) tracking path states to identify dependency loops."""
        visited: Set[str] = set()
        recursion_stack: Set[str] = set()

        def dfs_find_cycle(node: str) -> bool:
            visited.add(node)
            recursion_stack.add(node)

            for neighbor in self.graph.get(node, []):
                if neighbor not in visited:
                    if dfs_find_cycle(neighbor):
                        return True
                elif neighbor in recursion_stack:
                    return True # Graph cycle detected, indicating a deadlock condition

            recursion_stack.remove(node)
            return False

        for node in list(self.graph.keys()):
            if node not in visited:
                if dfs_find_cycle(node):
                    return True
        return False


if __name__ == "__main__":
    # Case A: A circular dependency deadlock loop (Node1 waits for Node2, which waits for Node1)
    deadlocked_cluster = {
        "node-A": ["node-B"],
        "node-B": ["node-A"]
    }
    detector = DistributedDeadlockGraphDetector(deadlocked_cluster)
    print(f"[DEADLOCK-CHECK] Deadlock detected? -> {detector.contains_circular_deadlock()}")