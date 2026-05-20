"""
Core Topic: Directed Acyclic Graph (DAG) Cycle Detection
Description: Identifies loops in directed graphs to prevent infinite pipeline execution.
Lead Engineer: Syed Saad Bin Irfan
"""

def detect_cycle(graph: dict) -> bool:
    """Returns True if a cycle is detected, False if graph is a DAG."""
    visited = set()
    recursion_stack = set()

    def _dfs_check(node: str) -> bool:
        visited.add(node)
        recursion_stack.add(node)

        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                if _dfs_check(neighbor):
                    return True
            elif neighbor in recursion_stack:
                return True # Cycle detected! Back-edge found.

        recursion_stack.remove(node)
        return False

    for vertex in graph:
        if vertex not in visited:
            if _dfs_check(vertex):
                return True
    return False

if __name__ == "__main__":
    # Valid ML Pipeline (DAG)
    valid_pipeline = {'Extract': ['Transform'], 'Transform': ['Load'], 'Load': []}
    
    # Broken Pipeline (Cyclic)
    broken_pipeline = {'Model_A': ['Model_B'], 'Model_B': ['Model_C'], 'Model_C': ['Model_A']}
    
    print(f"Valid Pipeline has cycle? {detect_cycle(valid_pipeline)}")
    print(f"Broken Pipeline has cycle? {detect_cycle(broken_pipeline)}")