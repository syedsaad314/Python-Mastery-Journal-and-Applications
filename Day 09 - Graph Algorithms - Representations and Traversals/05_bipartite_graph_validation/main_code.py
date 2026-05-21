"""
Core Topic: Bipartite Graph Vertex Coloring Validation
Description: Using two distinct color states to verify node partitions via BFS.
Lead Engineer: Syed Saad Bin Irfan
GitHub: https://github.com/syedsaad314
LinkedIn: https://www.linkedin.com/in/syed-saad-bin-irfan
"""

from collections import deque

class BipartiteValidator:
    @staticmethod
    def verify_two_color_partition(graph: dict[int, list[int]]) -> bool:
        """Verifies if a graph can be cleanly split into two non-overlapping groups."""
        color_assignments = {}  # Tracks color state maps (0 or 1)

        for node in graph:
            if node not in color_assignments:
                # Initialize unvisited node segments
                color_assignments[node] = 0
                queue = deque([node])

                while queue:
                    current = queue.popleft()
                    current_color = color_assignments[current]
                    next_color = 1 - current_color  # Flip color state cleanly (0 -> 1 or 1 -> 0)

                    for neighbor in graph.get(current, []):
                        if neighbor not in color_assignments:
                            color_assignments[neighbor] = next_color
                            queue.append(neighbor)
                        elif color_assignments[neighbor] == current_color:
                            # Conflict found: adjacent nodes share the same color partition
                            return False
        return True

if __name__ == "__main__":
    # Clean bipartite square network configuration
    valid_bipartite_network = {
        0: [1, 3],
        1: [0, 2],
        2: [1, 3],
        3: [0, 2]
    }
    
    is_valid = BipartiteValidator.verify_two_color_partition(valid_bipartite_network)
    print(f"Bipartite Cluster Partition Verification Status: {is_valid}")