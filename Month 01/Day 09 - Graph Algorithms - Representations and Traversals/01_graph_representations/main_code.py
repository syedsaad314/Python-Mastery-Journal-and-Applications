"""
Core Topic: Graph Representation Conversions
Description: Mapping network connections dynamically across lists and matrices.
Lead Engineer: Syed Saad Bin Irfan
GitHub: https://github.com/syedsaad314
LinkedIn: https://www.linkedin.com/in/syed-saad-bin-irfan
"""

class GraphSchemaConverter:
    @staticmethod
    def list_to_matrix(adjacency_list: dict[int, list[int]], total_nodes: int) -> list[list[int]]:
        """Transforms an Adjacency List into a flat lookup Adjacency Matrix."""
        matrix = [[0] * total_nodes for _ in range(total_nodes)]
        for source_node, edges in adjacency_list.items():
            for target_node in edges:
                matrix[source_node][target_node] = 1
        return matrix

    @staticmethod
    def matrix_to_list(matrix: list[list[int]]) -> dict[int, list[int]]:
        """Transforms an Adjacency Matrix back into a dynamic memory Adjacency List."""
        adjacency_list = {}
        for r_idx, row in enumerate(matrix):
            adjacency_list[r_idx] = []
            for c_idx, cell in enumerate(row):
                if cell == 1:
                    adjacency_list[r_idx].append(c_idx)
        return adjacency_list

if __name__ == "__main__":
    # 4 nodes connected via directional routes
    source_list = {
        0: [1, 2],
        1: [2],
        2: [0, 3],
        3: []
    }
    
    matrix_view = GraphSchemaConverter.list_to_matrix(source_list, total_nodes=4)
    print("Generated Adjacency Matrix Structure:")
    for row in matrix_view:
        print(f"  {row}")
        
    rebuilt_list = GraphSchemaConverter.matrix_to_list(matrix_view)
    print(f"\nRecovered Adjacency List Map: {rebuilt_list}")