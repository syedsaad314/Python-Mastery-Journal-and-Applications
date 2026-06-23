# Lead Engineer: Syed Saad Bin Irfan
"""
System: Reconciled Key-Value Store Entry Point
Description: Simulates out-of-sync cluster states and runs log reconciliation.
"""

from node import ClusterStoreNode
from network import NetworkMeshRouter
from metrics import StorageTelemetryPanel

def main() -> None:
    leader_node = ClusterStoreNode("node_primary_01", is_leader=True)
    follower_node_a = ClusterStoreNode("node_follower_02", is_leader=False)
    follower_node_b = ClusterStoreNode("node_follower_03", is_leader=False)
    
    leader_node.current_term = 3
    follower_node_a.current_term = 3
    follower_node_b.current_term = 3

    leader_node.storage.append_raw_entry(1, "SET user=saad")
    leader_node.storage.append_raw_entry(2, "SET access=admin")
    
    follower_node_a.storage.append_raw_entry(1, "SET user=saad")
    follower_node_a.storage.append_raw_entry(2, "SET access=admin")

    follower_node_b.storage.append_raw_entry(1, "SET user=saad")
    follower_node_b.storage.append_raw_entry(1, "SET access=guest")
    follower_node_b.storage.append_raw_entry(2, "SET workspace=temp")

    cluster_pool = [leader_node, follower_node_a, follower_node_b]
    router = NetworkMeshRouter(cluster_pool)

    print("--- Simulating Partitoned Cluster State Prior to Reconciliation ---")
    leader_node.commit_index = 1
    leader_node.storage.rebuild_state_machine(leader_node.commit_index)
    follower_node_a.commit_index = 1
    follower_node_a.storage.rebuild_state_machine(follower_node_a.commit_index)
    follower_node_b.commit_index = 2
    follower_node_b.storage.rebuild_state_machine(follower_node_b.commit_index)
    
    StorageTelemetryPanel.render_cluster_state(cluster_pool)

    router.broadcast_leader_write(leader_node, "SET status=active")

    print("\n--- Cluster State Post Log Reconciliation Verification ---")
    StorageTelemetryPanel.render_cluster_state(cluster_pool)

if __name__ == "__main__":
    main()