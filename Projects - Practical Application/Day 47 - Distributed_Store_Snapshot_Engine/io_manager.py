# Lead Engineer: Syed Saad Bin Irfan
"""
Portfolio Layer: Atomic Disk File Write Managers
"""
import os
import hashlib

class AtomicIOManager:
    @staticmethod
    def persist_atomic_payload(target_path: str, payload_bytes: bytes) -> str:
        temporary_working_path = f"{target_path}.tmp"
        
        # Enforce strict transaction level atomic isolation to protect against mid-write corruption
        with open(temporary_working_path, "wb") as disk_file:
            disk_file.write(payload_bytes)
            disk_file.flush()
            os.fsync(disk_file.fileno())
            
        os.replace(temporary_working_path, target_path)
        return hashlib.sha256(payload_bytes).hexdigest()