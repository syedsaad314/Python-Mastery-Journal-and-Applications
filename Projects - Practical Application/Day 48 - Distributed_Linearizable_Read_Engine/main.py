# Lead Engineer: Syed Saad Bin Irfan
"""
Portfolio Layer: System Runtime Harness & Performance Telemetry Simulator
"""
import time
from models import ClientRequest
from orchestrator import LinearizableEngineOrchestrator
from tabulate import tabulate # type: ignore

def main() -> None:
    cluster_nodes = ["node_1", "node_2", "node_3"]
    orchestrator = LinearizableEngineOrchestrator(cluster_nodes)

    print("=========================================================================")
    print("      INITIALIZING DEMONSTRATION RUN: LINEARIZABLE READ ENGINE           ")
    print("=========================================================================")

    # 1. Simulate High-Speed Optimized Lease Reads
    print("\n[SCENARIO 1] Granting and using leader lease allocation fields...")
    orchestrator.lease_mgr.trigger_grant_renewal() # Grant lease
    
    read_res_1 = orchestrator.process_linearizable_read("developer_profile", mock_active_network_acks=[])
    
    # 2. Simulate Lease Expiration Fallback
    print("\n[SCENARIO 2] Simulating lease expiration and consensus fallbacks...")
    time.sleep(2.0) # Force lease timeout expiration
    
    # Attempt read with successful quorum response acks
    read_res_2 = orchestrator.process_linearizable_read(
        "system_tier", 
        mock_active_network_acks=["node_1", "node_2"]
    )
    
    # Attempt read with failing quorum response acks (simulating network split-brain isolation)
    read_res_3 = orchestrator.process_linearizable_read(
        "cluster_health", 
        mock_active_network_acks=["node_1"]
    )

    # 3. Simulate Client Session Idempotency
    print("\n[SCENARIO 3] Verifying client request deduplication rules...")
    client_write_job = ClientRequest(client_id="saad_user_01", sequence_id=9901, payload="SET database_epoch=2026")
    
    write_initial = orchestrator.process_mutation_transaction(client_write_job)
    write_duplicate = orchestrator.process_mutation_transaction(client_write_job)

    # Compile and display system telemetry report
    telemetry_summary_table = [
        ["Scenario 1: Active Lease Read", read_res_1["read_strategy"], read_res_1["data"], read_res_1["latency_profile"]],
        ["Scenario 2: Expired Lease (Quorum Pass)", read_res_2["read_strategy"], read_res_2["data"], read_res_2["latency_profile"]],
        ["Scenario 2: Expired Lease (Quorum Fail)", read_res_3["read_strategy"], read_res_3["data"], read_res_3["latency_profile"]],
        ["Scenario 3: Initial Client Mutation Request", write_initial["execution_status"], f"Payload Result: {write_initial['result']}", f"Retried: {write_initial['retried']}"],
        ["Scenario 3: Duplicate Retried Request Call", write_duplicate["execution_status"], f"Payload Result: {write_duplicate['result']}", f"Retried: {write_duplicate['retried']}"]
    ]

    print("\n" + "="*85)
    print("                      SYSTEM TELEMETRY METRIC ANALYSIS REPORT             ")
    print("="*85)
    print(tabulate(
        telemetry_summary_table, 
        headers=["Operational Phase Action Description", "Strategy/Status Flag", "Resolved Value Data Output", "Performance Profile Latency Weight"], 
        tablefmt="fancy_grid"
    ))

if __name__ == "__main__":
    main()