# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Strided Array Window Views
Description: Demonstrates low-level numpy array strides to construct sliding windows
             and sub-grid views without duplicating underlying contiguous memory buffers.
"""
import numpy as np  # type: ignore[import-not-found]

class StridedArrayEngine:
    @staticmethod
    def create_sliding_window_1d(arr: np.ndarray, window_size: int) -> np.ndarray:
        if arr.ndim != 1:
            raise ValueError("Input array must be 1-dimensional.")
        if window_size > len(arr):
            raise ValueError("Window size cannot exceed total array length.")
            
        element_bytes = arr.strides[0]
        out_shape = (len(arr) - window_size + 1, window_size)
        out_strides = (element_bytes, element_bytes)
        
        # Re-interpret contiguous RAM memory via stride tricks without reallocation
        return np.lib.stride_tricks.as_strided(arr, shape=out_shape, strides=out_strides)

if __name__ == "__main__":
    data_stream = np.array([10, 20, 30, 40, 50], dtype=np.int64)
    windows = StridedArrayEngine.create_sliding_window_1d(data_stream, window_size=3)
    
    # Verify shape and zero-copy pointer properties
    assert windows.shape == (3, 3)
    assert np.array_equal(windows[0], [10, 20, 30])
    assert windows.base is data_stream # Validates zero-copy view pointer back to base
    
    print(f"[TASK 01 PASSED] Zero-copy sliding window generated successfully:\n{windows}")