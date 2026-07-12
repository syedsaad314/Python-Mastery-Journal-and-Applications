# Lead Engineer: Syed Saad Bin Irfan
"""
Portfolio Layer: Two-Phase Commit Simulation Verification Harness
"""
from network_stub import LatencyAwareNetworkFabric
from participant_node import TransactionParticipantNode
from coordinator import TwoPhaseCommitCoordinator
from tabulate import tabulate # type: ignore

def render_cluster_transaction_matrix(title: str, nodes: list[TransactionParticipantNode]) -> None:
    print(f"\n--- {title} ---")
    headers = ["Participant Node ID", "Active Storage Map", "Active Workspace Locks", "Write-Ahead Log History"]
    rows = []
    for node in nodes:
        rows.append([
            node.node_id, 
            str(node.active_data_store), 
            str(node.isolated_workspaces), 
            " -> ".join(node.durable_wal_log[-3:]) if node.durable_wal_log else "EMPTY"
        ])
    print(tabulate(rows, headers=headers, tablefmt="fancy_grid"))

def main() -> None:
    print("=========================================================================")
    print("        RUNNING ACTIVATION TRACK: DISTRIBUTED TWO-PHASE COMMIT           ")
    print("=========================================================================")

    # Initialize components
    network = LatencyAwareNetworkFabric()
    peer_ids = ["db_shard_01", "db_shard_02", "db_shard_03"]
    
    participants = [TransactionParticipantNode(node_id) for node_id in peer_ids]
    for p in participants:
        network.register_participant(p.node_id, p)
        
    coordinator = TwoPhaseCommitCoordinator(peer_ids, network)

    # -------------------------------------------------------------------------
    # SCENARIO 1: Unanimous Successful Transaction
    # -------------------------------------------------------------------------
    print("\n=== SCENARIO 1: Standard Successful Transaction Run ===")
    success = coordinator.execute_transaction("tx_alpha", "user_token", "active_session_data")
    assert success is True
    render_cluster_transaction_matrix("CLUSTER STATE AFTER SCENARIO 1 SUCCESS", participants)

    # -------------------------------------------------------------------------
    # SCENARIO 2: Node Rejection Triggering Global Rollback
    # -------------------------------------------------------------------------
    print("\n=== SCENARIO 2: Node Rejection & Automatic Abort Run ===")
    success = coordinator.execute_transaction("tx_beta", "account_balance", "TRIGGER_REJECTION_FAULT")
    assert success is False
    render_cluster_transaction_matrix("CLUSTER STATE AFTER SCENARIO 2 REJECTION (CLEAN WORKSPACES)", participants)

    # -------------------------------------------------------------------------
    # SCENARIO 3: Network Timeout Partition Handling
    # -------------------------------------------------------------------------
    print("\n=== SCENARIO 3: Network Timeout Partition & Abort Run ===")
    print("[NETWORK] Splitting db_shard_03 behind a network partition drop zone...")
    network.simulate_network_partition("db_shard_03")
    
    success = coordinator.execute_transaction("tx_gamma", "secure_vault_key", "unreachable_payload_data")
    assert success is False
    render_cluster_transaction_matrix("CLUSTER STATE AFTER SCENARIO 3 TIMEOUT (ROLLBACK EXECUTED)", participants)

if __name__ == "__main__":
    main()