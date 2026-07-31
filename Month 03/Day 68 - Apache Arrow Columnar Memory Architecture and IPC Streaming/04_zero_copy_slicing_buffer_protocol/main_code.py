# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Zero-Copy Array Slicing & Buffer Pointer Arithmetic
Description: Proves zero-copy execution during array slicing operations by verifying
             shared memory buffer addresses and length offsets.
"""
import pyarrow as pa  # type: ignore


class ZeroCopySlicer:
    @staticmethod
    def slice_array_zero_copy(arr: pa.Array, offset: int, length: int) -> tuple:
        # Slice array without copying physical memory buffers
        sliced_arr = arr.slice(offset, length)
        
        # Verify underlying buffer pointers match
        orig_buf_addr = arr.buffers()[1].address
        sliced_buf_addr = sliced_arr.buffers()[1].address
        
        return sliced_arr, (orig_buf_addr == sliced_buf_addr)


if __name__ == "__main__":
    original = pa.array([10, 20, 30, 40, 50, 60, 70], type=pa.int64())
    sliced, is_same_buffer = ZeroCopySlicer.slice_array_zero_copy(original, offset=2, length=3)
    
    assert is_same_buffer is True
    assert sliced.to_pylist() == [30, 40, 50]
    assert sliced.offset == 2
    
    print("[TASK 04 PASSED] Array sliced in constant time O(1) via shared buffer pointer offset.")