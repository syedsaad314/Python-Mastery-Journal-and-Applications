"""
Core Topic: Depth-First Search (DFS) for Deep State Exploration
Description: Utilizing the call stack (recursion) to explore graph branches to their absolute end before backtracking.
Lead Engineer: Syed Saad Bin Irfan
"""

def dfs_traverse(graph: dict, node: str, visited: set = None, path: list = None) -> list:
    """Recursively explores a graph, digging into branches until exhaustion."""
    if visited is None:
        visited = set()
    if path is None:
        path = []

    visited.add(node)
    path.append(node)

    for neighbor in graph.get(node, []):
        if neighbor not in visited:
            dfs_traverse(graph, neighbor, visited, path)
            
    return path

if __name__ == "__main__":
    # Representing a decision tree where we must explore deep consequences
    decision_tree = {
        'Start': ['Choice_1', 'Choice_2'],
        'Choice_1': ['Outcome_A', 'Outcome_B'],
        'Choice_2': ['Outcome_C'],
        'Outcome_A': [], 'Outcome_B': [], 'Outcome_C': []
    }
    
    exploration_path = dfs_traverse(decision_tree, 'Start')
    print(f"DFS Exploration Sequence: {exploration_path}")