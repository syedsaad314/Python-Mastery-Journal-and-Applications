"""
Core Topic: Connected Components & Network Clustering
Description: Scans an entire network graph to identify isolated groups or clusters.
Lead Engineer: Syed Saad Bin Irfan
"""

def find_clusters(graph: dict) -> list[list]:
    """Identifies all distinct, disconnected sub-graphs within a broader network."""
    visited = set()
    clusters = []

    def _explore_cluster(start_node: str) -> list:
        cluster_members = []
        stack = [start_node]
        
        while stack:
            node = stack.pop()
            if node not in visited:
                visited.add(node)
                cluster_members.append(node)
                stack.extend(graph.get(node, []))
                
        return cluster_members

    for vertex in graph:
        if vertex not in visited:
            # If vertex is unvisited, it belongs to a new, undiscovered cluster
            new_cluster = _explore_cluster(vertex)
            clusters.append(new_cluster)

    return clusters

if __name__ == "__main__":
    # A social network with two isolated friend groups
    social_graph = {
        'User_1': ['User_2', 'User_3'],
        'User_2': ['User_1'],
        'User_3': ['User_1'],
        'User_4': ['User_5'],
        'User_5': ['User_4']
    }
    
    groups = find_clusters(social_graph)
    print(f"Total Isolated Clusters Detected: {len(groups)}")
    for idx, group in enumerate(groups, 1):
        print(f"Cluster {idx}: {group}")