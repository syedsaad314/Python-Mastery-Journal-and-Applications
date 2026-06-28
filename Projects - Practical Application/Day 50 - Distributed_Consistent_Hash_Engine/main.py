# Lead Engineer: Syed Saad Bin Irfan
"""
Portfolio Layer: System Runtime Harness & Simulation Performance Logs
"""
from models import NodeConfig
from hash_ring import ConsistentHashRing
from tabulate import tabulate # type: ignore

def main() -> None:
    print("=========================================================================")
    print("      INITIALIZING DEMONSTRATION RUN: CONSISTENT HASH ENGINE           ")
    print("=========================================================================")

    ring_engine = ConsistentHashRing()

    # Register physical cluster nodes with different capacities
    node_configs = [
        NodeConfig(node_id="asia_host", max_capacity_weight=2, vnode_count=3),
        NodeConfig(node_id="europe_host", max_capacity_weight=4, vnode_count=3),
        NodeConfig(node_id="americas_host", max_capacity_weight=3, vnode_count=3)
    ]

    for config in node_configs:
        ring_engine.register_node(config)

    # -------------------------------------------------------------------------
    # SCENARIO 1: Standard Key Distribution and Replication Mapping
    # -------------------------------------------------------------------------
    print("\n[SCENARIO 1] Mapping incoming production keys across the ring...")
    sample_keys = ["user_saad_01", "session_token_xyz", "transaction_ledger_99", "api_key_vault"]
    results_matrix = []

    for key in sample_keys:
        res = ring_engine.resolve_key_placement(key, replication_factor=2)
        results_matrix.append([res.key, res.primary_node, str(res.replica_nodes), res.routing_strategy])

    print("\n" + "="*85)
    print("                      KEY PLACEMENT TELEMETRY REPORT                       ")
    print("=========================================================================")
    print(tabulate(results_matrix, headers=["Target Key ID", "Primary Assigned Host", "Replica Node Chain", "Routing Strategy Flag"], tablefmt="fancy_grid"))

    # -------------------------------------------------------------------------
    # SCENARIO 2: Bounded Load Reallocation Triggers
    # -------------------------------------------------------------------------
    print("\n[SCENARIO 2] Simulating traffic spike to trigger Bounded Load balancing...")
    # Flood the ring with matching keys to exhaust a node's capacity ceiling
    overload_tests = [f"flooded_key_index_{i}" for i in range(12)]
    overload_matrix = []

    for key in overload_tests:
        res = ring_engine.resolve_key_placement(key, replication_factor=1)
        overload_matrix.append([res.key, res.primary_node, res.routing_strategy])

    print("\n" + "="*85)
    print("                   BOUNDED LOAD STRUCTURAL TRAFFIC AUDIT                  ")
    print("=========================================================================")
    print(tabulate(overload_matrix, headers=["Target Key ID", "Assigned Destination Node", "Applied Routing Strategy"], tablefmt="fancy_grid"))

    # -------------------------------------------------------------------------
    # SCENARIO 3: Dynamic Node Eviction and Re-routing
    # -------------------------------------------------------------------------
    print("\n[SCENARIO 3] Evicting 'europe_host' to test dynamic cluster scaling...")
    ring_engine.remove_node("europe_host")
    
    post_eviction_res = ring_engine.resolve_key_placement("session_token_xyz", replication_factor=1)
    print(f"\n[MIGRATION-TELEMETRY] Key 'session_token_xyz' dynamically re-routed to: {post_eviction_res.primary_node}")

if __name__ == "__main__":
    main()