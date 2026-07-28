# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: C-Struct Byte Alignment in Structured NumPy Arrays
Description: Maps heterogenous byte-packed C-struct fields into continuous vectorized
             NumPy dtypes for low-overhead database and binary record parsing.
"""
import numpy as np # type: ignore

class StructuredArrayParser:
    # 4-byte int (sensor_id), 8-byte float (reading), 1-byte bool (is_valid)
    RECORD_DTYPE = np.dtype([
        ('sensor_id', np.int32),
        ('reading', np.float64),
        ('is_valid', np.bool_)
    ])

    @classmethod
    def parse_raw_binary_buffer(cls, raw_bytes: bytes) -> np.ndarray:
        return np.frombuffer(raw_bytes, dtype=cls.RECORD_DTYPE)

if __name__ == "__main__":
    # Create sample structured records
    records = np.array([
        (101, 36.5, True),
        (102, 41.2, False)
    ], dtype=StructuredArrayParser.RECORD_DTYPE)
    
    # Export to raw binary buffer and re-parse via zero-copy buffer casting
    raw_buffer = records.tobytes()
    parsed = StructuredArrayParser.parse_raw_binary_buffer(raw_buffer)
    
    assert len(parsed) == 2
    assert parsed['sensor_id'][0] == 101
    assert parsed['reading'][1] == 41.2
    assert parsed['is_valid'][0] == True
    
    print(f"[TASK 05 PASSED] Structured array parsed {len(parsed)} records from raw byte buffer.")