"""
Core Topic: Prim's Minimum Spanning Tree (MST)
Description: Greedy node-centric priority extraction to isolate dense backbone paths.
Lead Engineer: Syed Saad Bin Irfan
GitHub: https://github.com/syedsaad314
LinkedIn: https://www.linkedin.com/in/syed-saad-bin-irfan
"""

import heapq

class InfrastructurePrimsMST:
    @staticmethod
    def extract_minimum_spanning_tree(graph: dict[int, list[tuple[int, int]]], start_node: int = 0) -> list[tuple[int, int, int]]:
        """Constructs an optimized network backbone spanning tree using a vertex priority queue."""
        visited_nodes = set()
        minimum_spanning_tree_edges = []
        
        # Priority Queue tracking format: (edge_weight, source, target)
        edge_candidate_heap = [(0, -1, start_node)]
        
        while edge_candidate_heap:
            weight, source, target = heapq.heappop(edge_candidate_heap)
            
            if target in visited_nodes:
                continue
                
            visited_nodes.add(target)
            
            # Record the valid backbone connection (ignoring the initialization placeholder step)
            if source != -1:
                minimum_spanning_tree_edges.append((source, target, weight))
                
            for neighbor, edge_cost in graph.get(target, []):
                if neighbor not in visited_nodes:
                    heapq.heappush(edge_candidate_heap, (edge_cost, target, neighbor))
                    
        return minimum_spanning_tree_edges

if __name__ == "__main__":
    # Modeling backbone layout nodes connected via weighted links
    infrastructure_graph = {
        0: [(1, 2), (2, 3)],
        1: [(0, 2), (2, 1), (3, 4)],
        2: [(0, 3), (1, 1), (3, 5)],
        3: [(1, 4), (2, 5)]
    }
    
    mst_backbone = InfrastructurePrimsMST.extract_minimum_spanning_tree(infrastructure_graph, start_node=0)
    print(f"Isolated Prim's MST Infrastructure Backbone Edges: {mst_backbone}")