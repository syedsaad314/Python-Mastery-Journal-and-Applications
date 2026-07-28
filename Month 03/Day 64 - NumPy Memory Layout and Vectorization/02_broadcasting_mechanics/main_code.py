# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Zero-Memory Broadcasting Mechanics
Description: Explores NumPy broadcasting algorithms, demonstrating how array dimensions
             are expanded logically by setting stride steps to zero bytes.
"""
import numpy as np  # pyright: ignore[reportMissingImports]

class BroadcastingMechanicsEngine:
    @staticmethod
    def expand_dimension_zero_stride(vec: np.ndarray, target_rows: int) -> np.ndarray:
        if vec.ndim != 1:
            raise ValueError("Input must be a 1D vector.")
            
        # Reshape to (1, N) then broadcast to (target_rows, N)
        vec_2d = vec[np.newaxis, :]
        broadcasted = np.broadcast_to(vec_2d, (target_rows, vec.shape[0]))
        return broadcasted

if __name__ == "__main__":
    base_vector = np.array([1.0, 2.5, 4.0], dtype=np.float64)
    expanded_matrix = BroadcastingMechanicsEngine.expand_dimension_zero_stride(base_vector, target_rows=4)
    
    # Assert dimension expansion and zero-stride representation along axis 0
    assert expanded_matrix.shape == (4, 3)
    assert expanded_matrix.strides[0] == 0 # Zero stride means axis 0 reuses identical memory addresses!
    assert expanded_matrix.strides[1] == 8 # 8 bytes per float64
    
    print(f"[TASK 02 PASSED] Zero-stride broadcasting validated. Axis 0 Stride: {expanded_matrix.strides[0]} bytes.")