"""
CORE CONCEPT: Directed Acyclic Graph (DAG) Topological Processing Engine
Implementing Kahn's linear graph algorithm to determine execution order 
across asymmetric dependent tasks. Validates acyclic states to prevent structural deadlock.
"""

from collections import deque

class DAGExecutionEngine:
    def __init__(self, num_nodes: int):
        self.num_nodes = num_nodes
        # Initialize graph as a clean structural adjacency array lookup list
        self.adjacency_list: list[list[int]] = [[] for _ in range(num_nodes)]
        self.in_degree: list[int] = [0] * num_nodes

    def add_dependency_edge(self, source_node: int, destination_node: int) -> None:
        """Appends a directed node dependency connection to the execution matrix graph."""
        self.adjacency_list[source_node].append(destination_node)
        self.in_degree[destination_node] += 1

    def compute_topological_execution_order(self) -> list[int]:
        """Resolves structural execution sequence, raising an error if circular deadlocks are found."""
        execution_order = []
        # Tracking queue isolating processing nodes possessing zero unresolved input requirements
        zero_in_degree_queue = deque([i for i, degree in enumerate(self.in_degree) if degree == 0])

        while zero_in_degree_queue:
            current_node = zero_in_degree_queue.popleft()
            execution_order.append(current_node)

            for neighbor in self.adjacency_list[current_node]:
                self.in_degree[neighbor] -= 1
                if self.in_degree[neighbor] == 0:
                    zero_in_degree_queue.append(neighbor)

        if len(execution_order) != self.num_nodes:
            raise ValueError("Circular dependency constraint encountered; graph contains cyclic loops.")

        return execution_order


if __name__ == "__main__":
    # Creating a 4-layer computational network topology
    # Node 0 (Load Data) -> Node 1 (Feature Extraction) & Node 2 (Normalize Constraints) -> Node 3 (Train Model)
    engine = DAGExecutionEngine(num_nodes=4)
    engine.add_dependency_edge(0, 1)
    engine.add_dependency_edge(0, 2)
    engine.add_dependency_edge(1, 3)
    engine.add_dependency_edge(2, 3)

    print(f"Resolved Linear Model Execution Pipeline Sequence: {engine.compute_topological_execution_order()}")