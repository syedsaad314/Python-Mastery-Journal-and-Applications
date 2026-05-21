"""
Core Topic: Kahn's Topological Sort Algorithm
Description: Using node in-degree counts to resolve task dependency chains.
Lead Engineer: Syed Saad Bin Irfan
GitHub: https://github.com/syedsaad314
LinkedIn: https://www.linkedin.com/in/syed-saad-bin-irfan
"""

from collections import deque

class BuildScheduler:
    @staticmethod
    def compute_compilation_order(total_packages: int, prerequisites: list[tuple[int, int]]) -> list[int]:
        """Arranges tasks in a safe order by continuously processing nodes with zero incoming dependencies."""
        adjacency_list = {i: [] for i in range(total_packages)}
        indegree_map = [0] * total_packages

        # Step 1: Map connections and count incoming dependencies (in-degrees)
        for target, source in prerequisites:
            adjacency_list[source].append(target)
            indegree_map[target] += 1

        # Step 2: Queue up all nodes that have zero prerequisites
        zero_dependency_queue = deque([i for i in range(total_packages) if indegree_map[i] == 0])
        ordered_build_sequence = []

        # Step 3: Process nodes, decrementing neighbor dependencies as we go
        while zero_dependency_queue:
            current_node = zero_dependency_queue.popleft()
            ordered_build_sequence.append(current_node)

            for neighbor in adjacency_list[current_node]:
                indegree_map[neighbor] -= 1
                if indegree_map[neighbor] == 0:
                    zero_dependency_queue.append(neighbor)

        # If the output sequence length doesn't match total packages, a cycle exists
        if len(ordered_build_sequence) != total_packages:
            return []  # Invalid build matrix (hidden circular locking detected)
            
        return ordered_build_sequence

if __name__ == "__main__":
    # Task dependencies: (A, B) means B must finish before A can start
    dependency_rules = [(1, 0), (2, 0), (3, 1), (3, 2)]
    
    safe_order = BuildScheduler.compute_compilation_order(total_packages=4, prerequisites=dependency_rules)
    print(f"Calculated Safe Linear Package Compilation Chain: {safe_order}")