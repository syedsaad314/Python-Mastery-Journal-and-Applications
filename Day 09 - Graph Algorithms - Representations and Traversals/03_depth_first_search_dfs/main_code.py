"""
Core Topic: Depth-First Search Path Analysis
Description: Detecting cycle deadlocks in directed graphs using state-tracking sets.
Lead Engineer: Syed Saad Bin Irfan
GitHub: https://github.com/syedsaad314
LinkedIn: https://www.linkedin.com/in/syed-saad-bin-irfan
"""

class DependencyCycleDetector:
    def __init__(self, graph: dict[int, list[int]]):
        self.graph = graph
        self.global_visited = set()
        self.recursion_stack = set()

    def contains_cycle(self) -> bool:
        """Triggers system-wide searches to isolate recursive loop anomalies."""
        for node in self.graph:
            if node not in self.global_visited:
                if self._has_cyclic_path(node):
                    return True
        return False

    def _has_cyclic_path(self, node: int) -> bool:
        """Explores paths deeply while monitoring active recursion stack paths."""
        self.global_visited.add(node)
        self.recursion_stack.add(node)

        for neighbor in self.graph.get(node, []):
            if neighbor not in self.global_visited:
                if self._has_cyclic_path(neighbor):
                    return True
            elif neighbor in self.recursion_stack:
                # Loop confirmed: neighbor is still processing inside this call branch
                return True

        self.recursion_stack.remove(node)
        return False

if __name__ == "__main__":
    # Node 2 points back to 0, forming a cyclical path dependency loop
    cyclic_dependencies = {
        0: [1],
        1: [2],
        2: [0]
    }
    
    analyzer = DependencyCycleDetector(cyclic_dependencies)
    print(f"Cycle Verification Matrix Result: {analyzer.contains_cycle()}")