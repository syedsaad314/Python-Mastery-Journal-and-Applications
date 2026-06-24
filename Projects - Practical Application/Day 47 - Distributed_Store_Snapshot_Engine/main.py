# Lead Engineer: Syed Saad Bin Irfan
"""
Portfolio Layer: Main Runtime Demonstration Harness Entrypoint
"""
import os
from orchestrator import SnapshotEngineOrchestrator
from recovery_agent import ClusterRecoveryAgent
from tabulate import tabulate # type: ignore

def render_telemetry(label: str, orchestrator: SnapshotEngineOrchestrator) -> None:
    print(f"\n--- {label} ---")
    data = [
        ["Active KV Store Map", str(orchestrator.kv_store)],
        ["RAM WAL Log Length", f"{len(orchestrator.wal_log)} entries"],
        ["RAM WAL Log Array", str(orchestrator.wal_log)],
        ["Snapshot File Size", f"{os.path.getsize(orchestrator.output_filepath)} bytes" if os.path.exists(orchestrator.output_filepath) else "NO FILE"]
    ]
    print(tabulate(data, headers=["System Metric", "Current Realtime Footprint State"], tablefmt="fancy_grid"))

def main() -> None:
    target_snapshot_path = "cluster_snapshot.bin"
    
    # Ensure clean slate runs
    if os.path.exists(target_snapshot_path):
        os.remove(target_snapshot_path)

    # Initialize engine with a restrictive byte threshold to easily demonstrate compaction triggers
    engine = SnapshotEngineOrchestrator(target_snapshot_path, max_byte_threshold=350)
    
    print("=========================================================================")
    print("      INITIALIZING DEMONSTRATION RUN: SYSTEM COMPACTION WAL ENGINE       ")
    print("=========================================================================")

    # Step 1: Ingest standard mutations
    engine.commit_transaction(0, 1, "db_node", "karachi_primary_01")
    engine.commit_transaction(1, 1, "cluster_status", "healthy")
    render_telemetry("STAGE 01: Low Volume Ingestion", engine)

    # Step 2: Flood transaction engine to push over threshold limit bounds
    print("\n[TRANS-BURST] Injecting heavy data keys to trigger compaction thresholds...")
    engine.commit_transaction(2, 2, "admin_user", "saad_bin_irfan_se_2028")
    engine.commit_transaction(3, 2, "security_hash", "9f86d081884c7d659a2feaa0c55ad015")
    
    # This commit will trip the size check and run log compaction
    engine.commit_transaction(4, 2, "network_mesh_epoch", "epoch_count_value_2026")
    render_telemetry("STAGE 02: Post Compaction Trigger (RAM Log Traversal Truncated)", engine)

    # Step 3: Simulate sudden engine crash reboot routines
    print("\n[CRASH] Simulating sudden power failure... Purging local engine RAM structures...")
    engine.kv_store.clear()
    engine.wal_log.clear()
    print("[RAM-CLEARED] In-memory database state is now completely empty.")
    
    # Recover from persistent disk image storage
    recovered_data = ClusterRecoveryAgent.hydrate_system_node(target_snapshot_path)
    engine.kv_store = recovered_data.get("state", {})
    
    render_telemetry("STAGE 03: Post Crash Recovery System Reload (Disk Hydrated)", engine)

if __name__ == "__main__":
    main()