"""
Core Topic: Euler Tour Tree Flattening
Description: Flattens hierarchical tree networks into linear array ranges via entry and exit counters.
Lead Engineer: Syed Saad Bin Irfan
GitHub: https://github.com/syedsaad314
LinkedIn: https://www.linkedin.com/in/syed-saad-bin-irfan
"""

from typing import Dict, List, Tuple

class EulerTour:
    def __init__(self, num_nodes: int, adjacency_list: Dict[int, List[int]], root: int = 0) -> None:
        self.adj: Dict[int, List[int]] = adjacency_list
        self.entry_times: List[int] = [0] * num_nodes
        self.exit_times: List[int] = [0] * num_nodes
        self.flat_tour: List[int] = []
        self._timer: int = 0
        
        # Execute traversal pass starting from configured root node
        self._execute_tour(root, -1)

    def _execute_tour(self, node: int, parent: int) -> None:
        """Runs a depth-first pass tracking logical entry and exit timer ticks."""
        self.entry_times[node] = self._timer
        self.flat_tour.append(node)
        self._timer += 1
        
        for neighbor in self.adj.get(node, []):
            if neighbor != parent:
                self._execute_tour(neighbor, node)
                
        self.exit_times[node] = self._timer - 1

    def get_subtree_range(self, node: int) -> Tuple[int, int]:
        """Returns the start and end indices of a node's subtree within the flattened array."""
        return self.entry_times[node], self.exit_times[node]


if __name__ == "__main__":
    # Graph structure layout:
    #       0
    #      / \
    #     1   2
    #    / \
    #   3   4
    tree = {
        0: [1, 2],
        1: [0, 3, 4],
        2: [0],
        3: [1],
        4: [1]
    }
    
    tour_manager = EulerTour(num_nodes=5, adjacency_list=tree, root=0)
    print(f"Flattened tree representation order: {tour_manager.flat_tour}")
    
    start, end = tour_manager.get_subtree_range(1)
    print(f"Subtree range for node 1 inside flat array: [{start} to {end}]")