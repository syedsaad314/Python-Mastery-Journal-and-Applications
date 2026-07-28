# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Zero-Allocation In-Place Universal Functions
Description: Minimizes garbage collector allocations during math transformations 
             by leveraging out-parameter buffers inside NumPy ufuncs.
"""
import numpy as np # type: ignore

class InplaceVectorEngine:
    @staticmethod
    def execute_inplace_pipeline(a: np.ndarray, b: np.ndarray, scalar: float) -> np.ndarray:
        # Performs: a = (a + b) * scalar directly inside pre-allocated 'a' buffer
        np.add(a, b, out=a)
        np.multiply(a, scalar, out=a)
        return a

if __name__ == "__main__":
    vec_a = np.array([1.0, 2.0, 3.0], dtype=np.float64)
    vec_b = np.array([4.0, 5.0, 6.0], dtype=np.float64)
    
    initial_memory_address = vec_a.ctypes.data
    
    result = InplaceVectorEngine.execute_inplace_pipeline(vec_a, vec_b, scalar=2.0)
    
    # Validate mathematical correctness: ([1,2,3] + [4,5,6]) * 2 = [10, 14, 18]
    assert np.array_equal(result, [10.0, 14.0, 18.0])
    # Validate that memory buffer location did not change (Zero new allocations)
    assert result.ctypes.data == initial_memory_address
    
    print("[TASK 04 PASSED] In-place ufunc execution pipeline verified with zero heap reallocations.")