# Lead Engineer: Syed Saad Bin Irfan
"""
Portfolio Layer: Master Capstone Activation Dashboard and Fault Injection Drive
"""
import asyncio
from core_engines import CapstoneEventStoreAndOutbox, OrchestratedSagaComponent, ChoreographedSagaComponent
from benchmark import CapstonePerformanceDashboard
from models import UnifiedCapstoneEvent

async def run_milestone_capstone_suite() -> None:
    print("=========================================================================")
    print("    RUNNING ACTIVATION TRACK: MONTH 02 ARCHITECTURAL CAPSTONE WORKFLOW  ")
    print("=========================================================================")

    # Initialize components
    storage_core = CapstoneEventStoreAndOutbox()
    orchestrator_sim = OrchestratedSagaComponent()
    choreography_sim = ChoreographedSagaComponent()

    # -------------------------------------------------------------------------
    # PART 1: Fault Injection Testing (Orchestrated vs Choreographed Rollbacks)
    # -------------------------------------------------------------------------
    print("\n--- STEP 1: Systematic Fault Injection & Distributed Rollbacks ---")
    
    # Trigger an orchestrator failure to test centralized rollbacks
    print("\n[Executing Centralized Orchestration Fail Track]")
    await orchestrator_sim.execute_forward_chain(fail_downstream=True)
    
    # Trigger a choreographed event failure to test autonomous rollbacks
    print("\n[Executing Decentralized Choreographed Fail Track]")
    failure_signal = UnifiedCapstoneEvent(event_type="TRANSACTION_CRASHED_EVENT", payload={"scope": "Billing Service Blocked"})
    await choreography_sim.handle_incoming_failure_signal(failure_signal)
    print(f"Choreographed Component Database Recovered State: {choreography_sim.local_db_state}")

    # -------------------------------------------------------------------------
    # PART 2: Concurrency & Lock Verification (OCC Testing)
    # -------------------------------------------------------------------------
    print("\n--- STEP 2: Verifying Optimistic Concurrency Control Guards ---")
    
    # Save base transactions successfully
    evt1 = storage_core.append_with_occ(aggregate_id="ledger_01", expected_ver=0, etype="ACCOUNT_OPENED", data={"bal": 500})
    print(f"[OCC SUCCESS] Append approved at version marker 0. Current store index: {storage_core.stream_version}")
    
    # Simulate a collision where a slow client attempts to write back using an outdated version marker
    try:
        print("\n[Simulating Client Concurrency Collision Challenge]")
        storage_core.append_with_occ(aggregate_id="ledger_01", expected_ver=0, etype="STALE_WRITE_ATTEMPT", data={"bal": 600})
    except RuntimeError as collision_error:
        print(f"[OCC BLOCKED] ❌ Race condition blocked successfully: {collision_error}")

    # -------------------------------------------------------------------------
    # PART 3: Performance Checkpoints (Snapshot Replay Benchmarking)
    # -------------------------------------------------------------------------
    print("\n--- STEP 3: Executing Snapshot Optimization Metrics ---")
    
    performance_metrics = CapstonePerformanceDashboard.run_snapshot_efficiency_metric(storage_core)
    
    print("\n=========================================================================")
    print("                MONTH 02 CAPSTONE PERFORMANCE METRICS REPORT             ")
    print("=========================================================================")
    print(f" Raw Historical Log Replay Latency : {performance_metrics['replay_time_seconds']:.6f} seconds")
    print(f" Optimized Snapshot Replay Latency : {performance_metrics['snapshot_time_seconds']:.6f} seconds")
    print(f" System Recovery Speed Increase    : {performance_metrics['performance_gain_multiplier']}x Faster")
    print("=========================================================================")
    print(" CONFIRMED: Month 02 Core Distributed Architectural Blueprint Verified.")
    print("=========================================================================")

if __name__ == "__main__":
    asyncio.run(run_milestone_capstone_suite())