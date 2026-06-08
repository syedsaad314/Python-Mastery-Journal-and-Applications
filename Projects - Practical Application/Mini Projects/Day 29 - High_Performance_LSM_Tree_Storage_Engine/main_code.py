"""
System: Embedded Log-Structured Merge-Tree (LSM-Tree) Key-Value Storage Engine
Description: A high-performance embedded database featuring write-ahead logging (WAL), 
             sorted memory tables (MemTables), sparse file indexing, and probabilistic bloom filters.
Lead Engineer: Syed Saad Bin Irfan
"""

import os
import struct
import binascii
import logging
from typing import Dict, List, Tuple, Any, Optional

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)s] (LSM-Core) %(message)s')

class LocalBloomFilterGate:
    def __init__(self, capacity: int = 100) -> None:
        self.size = capacity * 8
        self.bits = bytearray((self.size + 7) // 8)

    def add(self, key_str: str) -> None:
        h_val = binascii.crc32(key_str.encode()) & 0xFFFFFFFF
        idx = h_val % self.size
        self.bits[idx // 8] |= (1 << (idx % 8))

    def checking(self, key_str: str) -> bool:
        h_val = binascii.crc32(key_str.encode()) & 0xFFFFFFFF
        idx = h_val % self.size
        return (self.bits[idx // 8] & (1 << (idx % 8))) != 0


class EmbeddedLsmStorageEngine:
    """An integrated hybrid storage engine that coordinates log buffering, data persistence, and searching."""
    STRUCT_SIG = "!HH"
    SIG_SIZE = struct.calcsize(STRUCT_SIG)

    def __init__(self, data_root_directory: str = "./lsm_data_arena") -> None:
        self.root_dir = data_root_directory
        self.wal_path = os.path.join(data_root_directory, "commit_journal.wal")
        self.sst_path = os.path.join(data_root_directory, "active_generation_0.sst")
        
        if not os.path.exists(self.root_dir):
            os.makedirs(self.root_dir)

        self.memtable: Dict[str, str] = {}
        self.bloom_filter = LocalBloomFilterGate()
        self.sparse_file_index: Dict[str, int] = {}
        
        self._execute_boot_recovery_and_indexing()

    def _execute_boot_recovery_and_indexing(self) -> None:
        """Recovers in-memory states from the journal log and loads indexes from existing tables."""
        if os.path.exists(self.wal_path) and os.path.getsize(self.wal_path) > 0:
            logging.info("Discovered active WAL log file. Starting state reconstruction passes...")
            # Simple line recovery parser implementation for the multi-tiered system core
            with open(self.wal_path, "rb") as f:
                while True:
                    header = f.read(4)
                    if not header or len(header) < 4: break
                    k_l, v_l = struct.unpack(self.STRUCT_SIG, header)
                    k = f.read(k_l).decode()
                    v = f.read(v_l).decode()
                    self.memtable[k] = v
                    self.bloom_filter.add(k)

        if os.path.exists(self.sst_path):
            logging.info("Discovered existing SSTable. Generating sparse lookup index maps...")
            with open(self.sst_path, "rb") as f:
                offset = 0
                while True:
                    header = f.read(4)
                    if not header: break
                    k_l, v_l = struct.unpack(self.STRUCT_SIG, header)
                    k = f.read(k_l).decode()
                    f.seek(v_l, os.SEEK_CUR)
                    self.sparse_file_index[k] = offset
                    self.bloom_filter.add(k)
                    offset += self.SIG_SIZE + k_l + v_l

    def write(self, key: str, value: str) -> None:
        """Appends mutations to the transaction log before writing changes to the memory buffer."""
        k_bytes, v_bytes = key.encode(), value.encode()
        
        # Log the modification sequence directly into the write-ahead journal file
        with open(self.wal_path, "ab") as wal_file:
            wal_file.write(struct.pack(self.STRUCT_SIG, len(k_bytes), len(v_bytes)) + k_bytes + v_bytes)
            os.fsync(wal_file.fileno())

        self.memtable[key] = value
        self.bloom_filter.add(key)

        # Trigger an automated flush pass if the memory table hits its size threshold limit
        if len(self.memtable) >= 4:
            self.flush_memtable_to_disk()

    def flush_memtable_to_disk(self) -> None:
        """Flushes sorted memory records sequentially into an immutable disk table file."""
        logging.info("MemTable threshold limits reached. Executing generation-0 SSTable flush sequence...")
        sorted_elements = sorted(self.memtable.items(), key=lambda x: x[0])
        
        current_offset = 0
        new_sparse_index: Dict[str, int] = {}

        with open(self.sst_path, "wb") as sst_file:
            for idx, (k, v) in enumerate(sorted_elements):
                k_b, v_b = k.encode(), v.encode()
                sst_file.write(struct.pack(self.STRUCT_SIG, len(k_b), len(v_b)) + k_b + v_b)
                
                # Sample keys at regular intervals to build a sparse memory lookup index
                if idx % 2 == 0:
                    new_sparse_index[k] = current_offset
                current_offset += self.SIG_SIZE + len(k_b) + len(v_b)

        self.sparse_file_index = new_sparse_index
        self.memtable.clear()
        
        # Clear out the old write-ahead log journal file once changes are safely committed to disk
        if os.path.exists(self.wal_path):
            os.remove(self.wal_path)
        logging.info("SSTable flush sequence completed successfully. Write journal recycled.")

    def read(self, key: str) -> Optional[str]:
        """Queries the database by searching across active memory tables, filters, and disk files."""
        # Step 1: Search the volatile memory buffer first
        if key in self.memtable:
            logging.info("Data block located inside the active MemTable layer.")
            return self.memtable[key]

        # Step 2: Query the Bloom Filter to avoid useless disk searches if the key is missing
        if not self.bloom_filter.checking(key):
            logging.info("Bloom Filter confirms key is missing. Skipping disk search.")
            return None

        # Step 3: Use the sparse memory index to scan the target disk file block
        if os.path.exists(self.sst_path) and self.sparse_file_index:
            logging.info("Searching sparse index arrays to locate disk file block offsets...")
            sorted_index_keys = sorted(self.sparse_index_keys()) # Handle file sorting constraints safely
            
            base_offset = 0
            for idx_k in sorted_index_keys:
                if idx_k <= key: base_offset = self.sparse_file_index[idx_k]
                else: break

            with open(self.sst_path, "rb") as sst_file:
                sst_file.seek(base_offset)
                while True:
                    header = sst_file.read(4)
                    if not header: break
                    k_l, v_l = struct.unpack(self.STRUCT_SIG, header)
                    curr_k = sst_file.read(k_l).decode()
                    
                    if curr_k == key:
                        return sst_file.read(v_l).decode()
                    elif curr_k > key:
                        break # Key is missing due to sorted file constraints
                    else:
                        sst_file.seek(v_l, os.SEEK_CUR)
        return None

    def sparse_index_keys(self) -> List[str]:
        return list(self.sparse_file_index.keys())

    def purge_environment_data(self) -> None:
        """Cleans up database storage files safely during teardown."""
        if os.path.exists(self.wal_path): os.remove(self.wal_path)
        if os.path.exists(self.sst_path): os.remove(self.sst_path)
        if os.path.exists(self.root_dir): os.rmdir(self.root_dir)


if __name__ == "__main__":
    print("\n=== SYSTEM START: EMBEDDED HIGH-PERFORMANCE LSM STORAGE ENGINE ===\n")
    engine = EmbeddedLsmStorageEngine()

    # Write data entries to test database update pipelines
    engine.write("saad_id", "bsse_dev_2026")
    engine.write("ubit_core", "cs_department")
    engine.write("framework", "python_mastery_log")
    
    # Trigger an automated memory table flush by writing additional entries
    engine.write("scale_node", "lsm_tree_active_sector")

    print(f"\n[QUERY PASS-1] Requesting 'saad_id': {engine.read('saad_id')}")
    print(f"[QUERY PASS-2] Requesting 'missing_key': {engine.read('missing_key')}")

    engine.purge_environment_data()
    print("\n=== SYSTEM SHUTDOWN: LSM ENGINE CLEANED DOWN ===")