"""
Core Topic: Write-Ahead Logging (WAL) with Recovery State Playback
Description: Implements an append-only transaction log to guarantee persistence before mutations hit memory.
Lead Engineer: Syed Saad Bin Irfan
"""

import os
import struct
import binascii
from typing import Dict, Tuple, Optional

class WriteAheadLog:
    """Manages an append-only binary database transaction log file for crash recovery."""
    # Record structural signature: uint32 (CRC32 Checksum), uint16 (Key Length), uint16 (Val Length)
    HEADER_FORMAT = "!IHH"
    HEADER_SIZE = struct.calcsize(HEADER_FORMAT)

    def __init__(self, wal_filepath: str) -> None:
        self.filepath: str = wal_filepath
        # Open in append-binary mode with zero internal buffer buffering
        self.file_descriptor = open(wal_filepath, "a+b", buffering=0)

    def append_mutation(self, key: str, value: str) -> None:
        """Packs and flushes a state modification transaction record to the physical disk log."""
        key_bytes = key.encode('utf-8')
        val_bytes = value.encode('utf-8')
        
        # Calculate a data verification checksum over the operation payload values
        payload_data = key_bytes + val_bytes
        crc_checksum = binascii.crc32(payload_data) & 0xFFFFFFFF
        
        header = struct.pack(self.HEADER_FORMAT, crc_checksum, len(key_bytes), len(val_bytes))
        # Write packed fields sequentially to the disk storage path
        self.file_descriptor.write(header + payload_data)
        # Flush internal kernel buffers straight down to disk hardware blocks
        os.fsync(self.file_descriptor.fileno())

    def recover_memory_state(self) -> Dict[str, str]:
        """Parses the uncompressed log file sequentially to reconstruct the database state after a crash."""
        recovered_state_map: Dict[str, str] = {}
        if os.path.getsize(self.filepath) == 0:
            return recovered_state_map

        # Open a read pointer channel targeting the start of the log file
        read_ptr = open(self.filepath, "rb")
        while True:
            header_bytes = read_ptr.read(self.HEADER_SIZE)
            if not header_bytes or len(header_bytes) < self.HEADER_SIZE:
                break # Reached end of file
                
            crc_checksum, k_len, v_len = struct.unpack(self.HEADER_FORMAT, header_bytes)
            payload_bytes = read_ptr.read(k_len + v_len)
            
            # Verify data integrity using a local CRC32 recalculation pass
            if binascii.crc32(payload_bytes) & 0xFFFFFFFF != crc_checksum:
                raise ConnectionCorruptedError("Critical: Corrupted WAL record encountered during playback.") # type: ignore
                
            key = payload_bytes[:k_len].decode('utf-8')
            val = payload_bytes[k_len:].decode('utf-8')
            
            if val == "__TOMBSTONE_VAL__":
                if key in recovered_state_map: del recovered_state_map[key]
            else:
                recovered_state_map[key] = val
                
        read_ptr.close()
        return recovered_state_map

    def close(self) -> None:
        if not self.file_descriptor.closed:
            self.file_descriptor.close()


if __name__ == "__main__":
    log_path = "system_mutation_journal.wal"
    print("[WAL-CORE] Initializing append-only transaction logging engine...")
    wal = WriteAheadLog(log_path)

    wal.append_mutation("account_2026", "active_tier")
    wal.append_mutation("node_cluster_id", "ubit_zone_alpha")

    print("[WAL-CORE] Simulating system crash. Replaying WAL logs to rebuild memory structures...")
    recovered_map = wal.recover_memory_state()
    print(f"[WAL-CORE] Reconstructed In-Memory Map State: {recovered_map}")
    
    wal.close()
    if os.path.exists(log_path): os.remove(log_path)