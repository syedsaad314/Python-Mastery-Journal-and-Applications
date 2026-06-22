"""
Core Topic: WAL-Backed Consensus Log Systems
Description: Persists distributed consensus log records to an append-only binary journal.
Lead Engineer: Syed Saad Bin Irfan
"""

import struct
import os
from typing import List, Tuple, Optional

class WalBackedConsensusLog:
    """Saves and restores consensus log paths using binary file operations."""
    RECORD_SIGNATURE = "!II" # Format: uint32 (Log Term Number), uint32 (Payload Size)
    SIG_SIZE = struct.calcsize(RECORD_SIGNATURE)

    def __init__(self, log_filepath: str) -> None:
        self.filepath: str = log_filepath
        self.file_descriptor = open(log_filepath, "a+b", buffering=0)

    def write_consensus_entry(self, term: int, command: str) -> None:
        """Appends a single consensus record cleanly to the binary file on disk."""
        payload_bytes = command.encode('utf-8')
        header = struct.pack(self.RECORD_SIGNATURE, term, len(payload_bytes))
        
        self.file_descriptor.write(header + payload_bytes)
        os.fsync(self.file_descriptor.fileno())

    def recover_consensus_history(self) -> List[Tuple[int, str]]:
        """Parses the binary file sequentially to restore log histories during node reboots."""
        history: List[Tuple[int, str]] = []
        if not os.path.exists(self.filepath) or os.path.getsize(self.filepath) == 0:
            return history

        with open(self.filepath, "rb") as reader:
            while True:
                header_bytes = reader.read(self.SIG_SIZE)
                if not header_bytes or len(header_bytes) < self.SIG_SIZE: break
                
                term, payload_len = struct.unpack(self.RECORD_SIGNATURE, header_bytes)
                command_string = reader.read(payload_len).decode('utf-8')
                history.append((term, command_string))
        return history

    def close(self) -> None:
        if not self.file_descriptor.closed: self.file_descriptor.close()


if __name__ == "__main__":
    path = "consensus_journal.bin"
    print("[WAL-CONSENSUS] Initializing safe log persistence systems...")
    journal = WalBackedConsensusLog(path)

    journal.write_consensus_entry(term=1, command="SET connection_limit=5000")
    journal.write_consensus_entry(term=1, command="SET secure_mode=ON")

    print("[WAL-CONSENSUS] Rebuilding history matrix arrays from disk logs...")
    restored_history = journal.recover_consensus_history()
    print(f"[WAL-CONSENSUS] Restored History Matrix Array: {restored_history}")

    journal.close()
    if os.path.exists(path): os.remove(path)