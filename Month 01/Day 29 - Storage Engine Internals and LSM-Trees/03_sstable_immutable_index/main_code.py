"""
Core Topic: Sparse Indexing and Immutable SSTable Querying
Description: Implements sparse memory index arrays to search large binary files efficiently.
Lead Engineer: Syed Saad Bin Irfan
"""

import struct
import os
from typing import Dict, Optional, List

class ImmutableSSTableReader:
    """Uses a sparse in-memory index array to execute fast lookups over immutable data files on disk."""
    
    def __init__(self, sstable_filepath: str, sparse_interval: int = 2) -> None:
        self.filepath: str = sstable_filepath
        self.sparse_index: Dict[str, int] = {}
        self._generate_sparse_index_map(sparse_interval)

    def _generate_sparse_index_map(self, interval: int) -> None:
        """Scans the data file sequentially to index keys at specific intervals, minimizing memory usage."""
        if not os.path.exists(self.filepath): return
        
        file_desc = open(self.filepath, "rb")
        record_counter = 0
        current_byte_offset = 0

        while True:
            len_bytes = file_desc.read(4)
            if not len_bytes or len(len_bytes) < 4: break
                
            k_len, v_len = struct.unpack("!HH", len_bytes)
            key_payload = file_desc.read(k_len)
            key = key_payload.decode('utf-8')
            
            # Skip past the value bytes block to find the next key header coordinate
            file_desc.seek(v_len, os.SEEK_CUR)
            
            # Record the file position index entry when hitting the interval step
            if record_counter % interval == 0:
                self.sparse_index[key] = current_byte_offset
                
            current_byte_offset += 4 + k_len + v_len
            record_counter += 1
            
        file_desc.close()

    def query_key(self, target_key: str) -> Optional[str]:
        """Searches the data file by locating the target key's bounded index block."""
        if not self.sparse_index: return None
        
        # Locate the closest matching index key block boundary entry
        sorted_indexed_keys = sorted(self.sparse_index.keys())
        candidate_base_offset: int = 0
        
        for idx_key in sorted_indexed_keys:
            if idx_key <= target_key:
                candidate_base_offset = self.sparse_index[idx_key]
            else:
                break # Target block boundary located

        # Scan the target file block sequentially from the base offset location
        f = open(self.filepath, "rb")
        f.seek(candidate_base_offset)
        
        while True:
            len_bytes = f.read(4)
            if not len_bytes: break
            k_len, v_len = struct.unpack("!HH", len_bytes)
            current_key = f.read(k_len).decode('utf-8')
            
            if current_key == target_key:
                val = f.read(v_len).decode('utf-8')
                f.close()
                return val
            elif current_key > target_key:
                break # Key is missing due to sorted file constraints
            else:
                f.seek(v_len, os.SEEK_CUR)
                
        f.close()
        return None


if __name__ == "__main__":
    # Setup mock raw file content entries manually to test lookup paths
    test_sst_file = "mock_table_block.sst"
    with open(test_sst_file, "wb") as mock_file:
        # Items must be appended in sorted order: 'device_0', 'device_1', 'device_2'
        for i in range(3):
            k, v = f"device_{i}".encode(), f"state_{i}".encode()
            mock_file.write(struct.pack("!HH", len(k), len(v)) + k + v)

    print("[SSTABLE-INDEX] Building reader engine and loading sparse index arrays...")
    reader = ImmutableSSTableReader(test_sst_file, sparse_interval=2)
    print(f"[SSTABLE-INDEX] Sparse Memory Maps Loaded: {reader.sparse_index}")

    outcome = reader.query_key("device_1")
    print(f"[SSTABLE-INDEX] Query Output: Key 'device_1' resolved value -> '{outcome}'")
    
    if os.path.exists(test_sst_file): os.remove(test_sst_file)