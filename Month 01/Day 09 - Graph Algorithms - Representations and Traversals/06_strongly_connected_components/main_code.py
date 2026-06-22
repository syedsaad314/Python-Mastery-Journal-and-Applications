"""
Core Topic: Kosaraju's Strongly Connected Components (SCC)
Description: Running a two-pass DFS to isolate independent loops in directed graphs.
Lead Engineer: Syed Saad Bin Irfan
GitHub: https://github.com/syedsaad314
LinkedIn: https://www.linkedin.com/in/syed-saad-bin-irfan
"""

class KosarajuSCCEngine:
    def __init__(self, total_nodes: int, edges: list[tuple[int, int]]):
        self.n = total_nodes
        self.graph = {i: [] for i in range(total_nodes)}
        self.transposed_graph = {i: [] for i in range(total_nodes)}
        
        # Build original graph and its transposed mirror simultaneously
        for source, target in edges:
            self.graph[source].append(target)
            self.transposed_graph[target].append(source)

    def _fill_order_stack(self, node: int, visited: set, stack: list) -> None:
        visited.add(node)
        for neighbor in self.graph[node]:
            if neighbor not in visited:
                self._fill_order_stack(neighbor, visited, stack)
        stack.append(node)

    def _collect_scc_nodes(self, node: int, visited: set, component: list) -> None:
        visited.add(node)
        component.append(node)
        for neighbor in self.transposed_graph[node]:
            if neighbor not in visited:
                self._collect_scc_nodes(neighbor, visited, component)

    def isolate_strongly_connected_loops(self) -> list[list[int]]:
        """Identifies and groups strongly connected components using a two-pass DFS."""
        processing_stack = []
        global_visited = set()

        # Pass 1: Gather nodes in a tracking stack based on their structural finish order
        for i in range(self.n):
            if i not in global_visited:
                self._fill_order_stack(i, global_visited, processing_stack)

        # Pass 2: Reverse edge directions and pull components off the stack
        global_visited.clear()
        consolidated_components = []

        while processing_stack:
            node = processing_stack.pop()
            if node not in global_visited:
                current_component = []
                self._collect_scc_nodes(node, global_visited, current_component)
                consolidated_components.append(current_component)

        return consolidated_components

if __name__ == "__main__":
    # Graph containing two separate structural loop sub-clusters
    edge_matrix = [(0, 1), (1, 2), (2, 0), (2, 3), (3, 4), (4, 3)]
    
    engine = KosarajuSCCEngine(total_nodes=5, edges=edge_matrix)
    scc_groups = engine.isolate_strongly_connected_loops()
    print(f"Isolated Strongly Connected Component Group Clusters: {scc_groups}")