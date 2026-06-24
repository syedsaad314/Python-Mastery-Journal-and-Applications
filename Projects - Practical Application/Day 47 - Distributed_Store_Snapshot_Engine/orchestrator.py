# Lead Engineer: Syed Saad Bin Irfan
"""
Portfolio Layer: Core Engine System State Orchestrator
"""
from models import StateSnapshotImage
from encoder import SnapshotEncoder
from io_manager import AtomicIOManager
from compaction_policy import SystemCompactionPolicy
from log_truncator import AdvancedLogTruncator

class SnapshotEngineOrchestrator:
    def __init__(self, output_filepath: str, max_byte_threshold: int) -> None:
        self.output_filepath = output_filepath
        self.policy = SystemCompactionPolicy(max_byte_threshold)
        self.kv_store = {}
        self.wal_log = []

    def commit_transaction(self, entry_index: int, entry_term: int, key: str, value: str) -> bool:
        # 1. Write to volatile write-ahead log
        log_packet = {"index": entry_index, "term": entry_term, "cmd": f"SET {key}={value}"}
        self.wal_log.append(log_packet)
        
        # 2. Mutate state engine store values
        self.kv_store[key] = value

        # 3. Check compaction threshold policies
        if self.policy.is_compaction_required(self.wal_log):
            print(f"\n[ORCHESTRATOR] Compaction policy triggered at index {entry_index}!")
            
            # Package state and serialize to binary
            snapshot_image = StateSnapshotImage(entry_index, entry_term, self.kv_store)
            packet = snapshot_image.compile_structural_packet()
            binary_data = SnapshotEncoder.export_to_binary_stream(packet)
            
            # Commit to disk atomically
            file_hash = AtomicIOManager.persist_atomic_payload(self.output_filepath, binary_data)
            print(f"[IO-SUCCESS] Snapshot written to disk. SHA256: {file_hash}")
            
            # Truncate memory logs
            self.wal_log = AdvancedLogTruncator.purge_below_boundary(self.wal_log, entry_index)
            return True
        return False