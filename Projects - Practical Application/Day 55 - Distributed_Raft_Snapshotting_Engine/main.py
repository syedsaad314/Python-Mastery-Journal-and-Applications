# Lead Engineer: Syed Saad Bin Irfan
"""
Portfolio Layer: Snapshotting Logic Verification Test Harness
"""
from network_stub import ClusterNetworkFabric
from raft_node import RaftCompactionNode
from tabulate import tabulate # type: ignore

def render_cluster_snapshot_matrix(title: str, cluster: list[RaftCompactionNode]) -> None:
    print(f"\n--- {title} ---")
    headers = ["Node ID", "Role", "Commit Index", "Last Snapshot Index", "Memory Log Items Count", "State Map Snapshot"]
    rows = []
    for node in cluster:
        rows.append([
            node.node_id, node.role, node.commit_index, 
            node.last_included_index, len(node.log), str(node.state_machine.storage)
        ])
    print(tabulate(rows, headers=headers, tablefmt="fancy_grid"))

def main() -> None:
    print("=========================================================================")
    print("        RUNNING ACTIVATION TRACK: RAFT LOG COMPACTION & SNAPSHOTS        ")
    print("=========================================================================")

    net = ClusterNetworkFabric()
    ids = ["srv_01", "srv_02", "srv_03"]
    
    cluster = [RaftCompactionNode(i, ids, net) for i in ids]
    for node in cluster:
        net.register_node(node.node_id, node)

    leader = cluster[0]
    leader.role = "LEADER"
    for peer in ids:
        if peer != leader.node_id:
            leader.next_index[peer] = 1
            leader.match_index[peer] = 0

    # 1. Populate log history across the cluster
    print("\n[STEP 1] Appending and replicating a series of client updates...")
    for idx, char in enumerate(["A", "B", "C", "D"], start=1):
        leader.log.append(LogEntry(term=1, index=idx, command={"op": "SET", "key": f"key_{char}", "val": idx * 10})) # type: ignore
        leader.commit_index = idx
        leader.apply_committed_logs()
        for p in ["srv_02", "srv_03"]:
            leader.replicate_to_peer(p)

    render_cluster_snapshot_matrix("STATE BEFORE LOG COMPACTION", cluster)

    # 2. Trigger compaction on the leader node
    print("\n[STEP 2] Leader triggers compaction up to index 2...")
    leader.compact_log_buffer(clean_up_to_idx=2)
    render_cluster_snapshot_matrix("STATE AFTER LEADER LOG COMPACTION", cluster)

    # 3. Simulate a lagging node rejoining the cluster
    print("\n[STEP 3] Introducing a highly lagging node (srv_03 reset to index 0)...")
    leader.next_index["srv_03"] = 1
    
    print("Leader replicates updates to srv_03; should trigger an InstallSnapshot flow...")
    leader.replicate_to_peer("srv_03")

    render_cluster_snapshot_matrix("FINAL CLUSTER STATE: LAGGING NODE CAUGHT UP VIA SNAPSHOT", cluster)

if __name__ == "__main__":
    main()