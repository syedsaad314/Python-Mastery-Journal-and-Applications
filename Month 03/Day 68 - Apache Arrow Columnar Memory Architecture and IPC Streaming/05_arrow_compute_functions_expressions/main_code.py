# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: SIMD-Accelerated PyArrow C++ Compute Kernels
Description: Executes vector operations natively using pyarrow.compute C++ kernels
             without materializing Python loops or NumPy conversions.
"""
import pyarrow as pa  # type: ignore
import pyarrow.compute as pc  # type: ignore


class ArrowComputeEngine:
    @staticmethod
    def filter_and_sum(arr: pa.Array, threshold: float) -> float:
        # Create boolean mask using vectorized SIMD compute kernel
        mask = pc.greater(arr, threshold)
        
        # Apply mask and aggregate sum
        filtered_arr = pc.filter(arr, mask)
        total_sum = pc.sum(filtered_arr)
        
        return total_sum.as_py()


if __name__ == "__main__":
    data_array = pa.array([12.5, 45.0, 3.2, 88.1, 100.0, 5.5], type=pa.float64())
    
    result_sum = ArrowComputeEngine.filter_and_sum(data_array, threshold=10.0)
    
    expected_sum = 12.5 + 45.0 + 88.1 + 100.0
    assert abs(result_sum - expected_sum) < 1e-5
    
    print(f"[TASK 05 PASSED] PyArrow C++ compute kernel calculated filtered sum: {result_sum:.2f}")