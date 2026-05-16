"""
CORE CONCEPT: Linear Algebra Foundations from Scratch
Implementing low-level vector dot product and multi-dimensional matrix 
multiplication algorithms using pure Python. This forms the structural bedrock 
of forward propagation loops in Neural Networks without using external engines.
"""

def vector_dot_product(vector_a: list[float], vector_b: list[float]) -> float:
    """Computes the dot product of two vectors with strict dimensionality assertion."""
    if len(vector_a) != len(vector_b):
        raise ValueError("Vector dimensions must match perfectly for a dot product.")
    
    return sum(a * b for a, b in zip(vector_a, vector_b))


def matrix_multiplication(matrix_a: list[list[float]], matrix_b: list[list[float]]) -> list[list[float]]:
    """Performs mathematical matrix multiplication (A x B) via vanilla control flows."""
    rows_a = len(matrix_a)
    cols_a = len(matrix_a[0])
    rows_b = len(matrix_b)
    cols_b = len(matrix_b[0])

    if cols_a != rows_b:
        raise ValueError(f"Incompatible dimensions: Matrix A columns ({cols_a}) must equal Matrix B rows ({rows_b}).")

    # Initialize empty result matrix with dimensions (rows_a x cols_b)
    result = [[0.0 for _ in range(cols_b)] for _ in range(rows_a)]

    # Compute dot product for every row-column combination
    for i in range(rows_a):
        for j in range(cols_b):
            # Extract column j from matrix_b
            column_b = [matrix_b[r][j] for r in range(rows_b)]
            result[i][j] = vector_dot_product(matrix_a[i], column_b)

    return result


if __name__ == "__main__":
    # Operational execution testing engineering soundness
    v1 = [1.0, 2.0, 3.0]
    v2 = [4.0, 5.0, 6.0]
    print(f"Executed Vector Dot Product: {vector_dot_product(v1, v2)}")

    mat_a = [[1, 2], [3, 4]]
    mat_b = [[5, 6], [7, 8]]
    print(f"Executed Matrix Multiplication: {matrix_multiplication(mat_a, mat_b)}")