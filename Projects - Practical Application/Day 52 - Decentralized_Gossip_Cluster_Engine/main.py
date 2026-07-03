# Lead Engineer: Syed Saad Bin Irfan
"""
Portfolio Layer: System Runtime Harness & Multi-Agent Cluster Sim Logs
"""
from gossip_node import DistributedGossipNode
from network_simulator import VirtualNetworkCluster
from tabulate import tabulate # type: ignore

def print_cluster_state(title: str, cluster: VirtualNetworkCluster) -> None:
    print(f"\n--- {title} ---")
    headers = ["Local Node ID", "Known Peer Node ID", "Last Heartbeat Vector", "Current Status"]
    table_rows = []
    
    for _, node_obj in cluster.live_nodes.items():
        is_first = True
        for peer_id, meta in sorted(node_obj.membership_registry.items()):
            node_label = node_obj.node_id + (" (ISOLATED)" if node_obj.node_id in cluster.dropped_nodes else "")
            table_rows.append([node_label, peer_id, meta["heartbeat"], meta["status"]])
            
    print(tabulate(table_rows, headers=headers, tablefmt="fancy_grid"))

def main() -> None:
    print("=========================================================================")
    print("      INITIALIZING DEMONSTRATION RUN: DECENTRALIZED GOSSIP ENGINE        ")
    print("=========================================================================")

    cluster = VirtualNetworkCluster()

    # Provision 3 physical nodes across the virtual domain
    node_A = DistributedGossipNode("node_10.0.0.1_A")
    node_B = DistributedGossipNode("node_10.0.0.2_B")
    node_C = DistributedGossipNode("node_10.0.0.3_C")

    cluster.attach_node(node_A)
    cluster.attach_node(node_B)
    cluster.attach_node(node_C)

    # 1. Bootstrapping Peer Discovery
    print("\n[SCENARIO 1] Nodes starting discovery cycles...")
    # Inject minimal initial connection pathways
    node_A.membership_registry["node_10.0.0.2_B"] = {"heartbeat": 0, "status": "ALIVE"}
    node_B.membership_registry["node_10.0.0.3_C"] = {"heartbeat": 0, "status": "ALIVE"}

    print_cluster_state("INITIAL STATES BEFORE GOSSIP INCUBATION", cluster)

    # Simulate gossip round trips
    for step in range(5):
        node_A.increment_local_heartbeat()
        node_B.increment_local_heartbeat()
        node_C.increment_local_heartbeat()
        
        cluster.route_gossip_step("node_10.0.0.1_A")
        cluster.route_gossip_step("node_10.0.0.2_B")
        cluster.route_gossip_step("node_10.0.0.3_C")

    print_cluster_state("CLUSTER CONVERGENCE: FULL STATE ADAPTATION SUCCESSFUL", cluster)

    # 2. Node Failure Event and Detection Sequences
    print("\n[SCENARIO 2] Simulating unexpected node failure on node_10.0.0.3_C...")
    cluster.isolate_node_from_network("node_10.0.0.3_C")

    # Let time advance and remaining nodes continue gossiping
    for tick in range(10, 18):
        node_A.increment_local_heartbeat()
        node_B.increment_local_heartbeat()
        
        cluster.route_gossip_step("node_10.0.0.1_A")
        cluster.route_gossip_step("node_10.0.0.2_B")

    print_cluster_state("STATES REFLECTING TIME LAPSE (NODE C HEARTBEATS ARE FROZEN)", cluster)

    # Trigger failure audits across healthy cluster components
    print("\n[SCENARIO 3] Running cluster liveness audits...")
    # Node A evaluates current state using tick index 17 as baseline comparison
    node_A.audit_and_detect_failures(failure_threshold_ticks=5, reference_tick=17)
    node_B.audit_and_detect_failures(failure_threshold_ticks=5, reference_tick=17)

    # Synchronize the failure discovery across the remaining cluster
    cluster.route_gossip_step("node_10.0.0.1_A")

    print_cluster_state("FINAL STATE DETECTED: DEAD NODE EVICTED FROM WORKFLOWS", cluster)

if __name__ == "__main__":
    main()