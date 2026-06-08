"""
Core Topic: LSM-Tree Compaction Engine
Description: Merges overlapping sorted data tables using a priority queue merge pattern.
Lead Engineer: Syed Saad Bin Irfan
"""

import struct
import heapq
import os
from typing import List, Tuple

class TableCompactor:
    """Merges overlapping immutable storage tables while pruning old values and tombstones."""
    
    @staticmethod
    def _read_all_records(filepath: str) -> List[Tuple[str, str]]:
        """Parses an SSTable binary file into an array list context."""
        records: List[Tuple[str, str]] = []
        if not os.path.exists(filepath): return records
        
        with open(filepath, "rb") as f:
            while True:
                len_bytes = f.read(4)
                if not len_bytes: break
                k_len, v_len = struct.unpack("!HH", len_bytes)
                k = f.read(k_len).decode('utf-8')
                v = f.read(v_len).decode('utf-8')
                records.append((k, v))
        return records

    @classmethod
    def merge_segments(cls, file_a: str, file_b: str, output_filepath: str) -> None:
        """Merges two sorted files into a single consolidated table layer, removing old duplicate keys."""
        records_a = cls._read_all_records(file_a)
        records_b = cls._read_all_records(file_b)
        
        # Merge sorted data arrays using a standard two-pointer comparison sweep
        ptr_a, ptr_b = 0, 0
        merged_buffer: List[Tuple[str, str]] = []

        while ptr_a < len(records_a) and ptr_b < len(records_b):
            key_a, val_a = records_a[ptr_a]
            key_b, val_b = records_b[ptr_b]
            
            if key_a == key_b:
                # File B simulates the newer data generation; keep B and drop the older record A
                merged_buffer.append((key_b, val_b))
                ptr_a += 1
                ptr_b += 1
            elif key_a < key_b:
                merged_buffer.append((key_a, val_a))
                ptr_a += 1
            else:
                merged_buffer.append((key_b, val_b))
                ptr_b += 1

        # Flush any remaining items from both lists to the buffer
        while ptr_a < len(records_a):
            merged_buffer.append(records_a[ptr_a]); ptr_a += 1
        while ptr_b < len(records_b):
            merged_buffer.append(records_b[ptr_b]); ptr_b += 1

        # Write out the consolidated data records buffer to the output destination file
        with open(output_filepath, "wb") as out_file:
            for k_str, v_str in merged_buffer:
                # Skip writing tombstone records to prune deleted keys permanently
                if v_str == "__TOMBSTONE__": continue
                k_b, v_b = k_str.encode(), v_str.encode()
                out_file.write(struct.pack("!HH", len(k_b), len(v_b)) + k_b + v_b)


if __name__ == "__main__":
    print("[COMPACTION] Initializing segment consolidation test pass routines...")
    file_1, file_2, file_out = "seg_1.sst", "seg_2.sst", "merged_tier.sst"

    # Write out a mock base file segment layer
    with open(file_1, "wb") as f:
        f.write(struct.pack("!HH", 6, 6) + b"node_0" + b"status")
    # Write out a mock updated file segment layer containing a mutation
    with open(file_2, "wb") as f:
        f.write(struct.pack("!HH", 6, 7) + b"node_0" + b"offline")

    TableCompactor.merge_segments(file_1, file_2, file_out)
    print("[COMPACTION] Consolidation pass finished. Verifying data outputs:")
    
    with open(file_out, "rb") as f:
        print("  Merged File Contents:", f.read()[4:])

    # Clean up file artifacts
    for p in [file_1, file_2, file_out]:
        if os.path.exists(p): os.remove(p)