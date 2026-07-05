# Lead Engineer: Syed Saad Bin Irfan
"""
Portfolio Layer: Cluster Execution Harness & Consensus Metrics Report
"""
from network_stub import MockNetworkBackplane
from raft_node import RaftConsensusNode
from tabulate import tabulate # type: ignore

def print_cluster_telemetry(title: str, cluster_nodes: list) -> None:
    print(f"\n--- {title} ---")
    headers = ["Node Identity Token", "Logical Term Counter", "Current Role Status", "Voted For Candidate", "Heartbeats Intercepted"]
    table_rows = []
    for node in cluster_nodes:
        table_rows.append([node.node_id, node.current_term, node.state, node.voted_for if node.voted_for else "NONE", node.heartbeats_received])
    print(tabulate(table_rows, headers=headers, tablefmt="fancy_grid"))

def main() -> None:
    print("=========================================================================")
    print("        INITIALIZING RUNTIME: DISTRIBUTED RAFT CONSENSUS ENGINE          ")
    print("=========================================================================")

    network = MockNetworkBackplane()

    # Provision a standard 3-node cluster
    nodes_list = [
        RaftConsensusNode("node_srv_01", network),
        RaftConsensusNode("node_srv_02", network),
        RaftConsensusNode("node_srv_03", network)
    ]

    for node in nodes_list:
        network.register_node_instance(node.node_id, node)

    print_cluster_telemetry("CLUSTER BOOTSTRAP STATE (ALL FOLLOWER BASELINE)", nodes_list)

    # -------------------------------------------------------------------------
    # SCENARIO 1: Simulating an Election Timeout and Leadership Race
    # -------------------------------------------------------------------------
    print("\n[SCENARIO 1] Node 1 times out first and initiates its campaign...")
    election_won = nodes_list[0].trigger_election_timeout(total_nodes=3)
    
    assert election_won == True
    assert nodes_list[0].state == "LEADER"
    print_cluster_telemetry("POST-ELECTION TELEMETRY METRICS", nodes_list)

    # -------------------------------------------------------------------------
    # SCENARIO 2: Heartbeat Distribution Cycle
    # -------------------------------------------------------------------------
    print("\n[SCENARIO 2] New leader begins broadcasting heartbeats to suppress peer elections...")
    from models import AppendEntriesHeartbeat
    
    leader = nodes_list[0]
    heartbeat_packet = AppendEntriesHeartbeat(term=leader.current_term, leader_id=leader.node_id)
    
    # Send two consecutive heartbeat updates
    network.broadcast_heartbeat(leader.node_id, heartbeat_packet)
    network.broadcast_heartbeat(leader.node_id, heartbeat_packet)

    print_cluster_telemetry("REPLICATED METRICS FOLLOWING HEARTBEAT BROADCASTS", nodes_list)

    # -------------------------------------------------------------------------
    # SCENARIO 3: Term Validation and Higher Term Ouster
    # -------------------------------------------------------------------------
    print("\n[SCENARIO 3] An isolated node returns with a higher logical term counter...")
    # Simulate an external node that incremented its term during a network partition
    nodes_list[2].current_term = 5 
    
    print("Node 3 triggers an election timeout under its higher term configuration...")
    nodes_list[2].trigger_election_timeout(total_nodes=3)

    print_cluster_telemetry("FINAL CONVEX STATE: NODE 1 DETECTS HIGHER TERM AND STEPS DOWN", nodes_list)

if __name__ == "__main__":
    main()