
# Lead Engineer: Syed Saad Bin Irfan
"""
Portfolio Layer: Distributed Log Replication Harness Runner
"""
from network_stub import SynchronousNetworkBackplane
from raft_node import RaftReplicationNode
from tabulate import tabulate # type: ignore

def render_cluster_log_matrix(title: str, cluster: list[RaftReplicationNode]) -> None:
    print(f"\n--- {title} ---")
    headers = ["Node Identity Token", "Role Profile", "Commit Index Pointer", "State Machine Value", "Internal Log Layout"]
    rows = []
    for node in cluster:
        log_summary = [f"Idx{e.index}(T{e.term}):{e.command['key']}={e.command['val']}" for e in node.log]
        val = node.state_machine.storage.get("cluster_key", "NOT_SET")
        rows.append([node.node_id, node.role, node.commit_index, f"cluster_key={val}", " -> ".join(log_summary) if log_summary else "EMPTY"])
    print(tabulate(rows, headers=headers, tablefmt="fancy_grid"))

def main() -> None:
    print("=========================================================================")
    print("        RUNNING ACTIVATION TRACK: DISTRIBUTED RAFT LOG REPLICATION       ")
    print("=========================================================================")

    net = SynchronousNetworkBackplane()
    node_identities = ["srv_01", "srv_02", "srv_03"]
    
    cluster_nodes = [
        RaftReplicationNode("srv_01", node_identities, net),
        RaftReplicationNode("srv_02", node_identities, net),
        RaftReplicationNode("srv_03", node_identities, net)
    ]
    
    for node in cluster_nodes:
        net.register_cluster_target(node.node_id, node)

    # -------------------------------------------------------------------------
    # SCENARIO 1: Standard Balanced Write Progression
    # -------------------------------------------------------------------------
    print("\n[SCENARIO 1] Node 1 claims leadership and handles client writes...")
    leader = cluster_nodes[0]
    leader.assume_leadership(term=1)
    
    leader.client_write_request({"op": "SET", "key": "cluster_key", "val": "alpha_release"})
    render_cluster_log_matrix("STATE AFTER SCENARIO 1 REPLICATION", cluster_nodes)

    # -------------------------------------------------------------------------
    # SCENARIO 2: Follower Alignment Truncation Resolution
    # -------------------------------------------------------------------------
    print("\n[SCENARIO 2] Simulating conflict resolution for out-of-sync followers...")
    # Inject a conflicting entry directly into Node 3's log to simulate an uncommitted split-brain write
    from models import LogEntry
    bad_entry = LogEntry(term=2, index=2, command={"op": "SET", "key": "cluster_key", "val": "rogue_data"})
    cluster_nodes[2].log.append(bad_entry)
    cluster_nodes[2].current_term = 2
    
    render_cluster_log_matrix("INTERMEDIARY MIXED STATE (NODE 3 CONTAINS UNCOMMITTED CONFLICT)", cluster_nodes)

    # Node 1 issues a fresh write command, forcing an alignment sweep down the network
    print("\nLeader handles a new client write, triggering a log alignment check across all nodes...")
    leader.client_write_request({"op": "SET", "key": "cluster_key", "val": "production_stable"})
    
    render_cluster_log_matrix("FINAL RECONCILED CONVEX STATE (CONFLICTS TRUNCATED & ALIGNED)", cluster_nodes)

if __name__ == "__main__":
    main()