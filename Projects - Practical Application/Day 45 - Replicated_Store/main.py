"""
System: Replicated Key-Value Store Entry Point
Description: Sets up a multi-node cluster, triggers leader elections, and processes consensus data writes.
Lead Engineer: Syed Saad Bin Irfan
"""

from node import ClusterConsensusNode
from cluster import ClusterCommunicationMesh
from metrics import ClusterMetricsDashboard

def main() -> None:
    # 1. Initialize a 5-node consensus cluster
    cluster_nodes = [
        ClusterConsensusNode("node_host_01"),
        ClusterConsensusNode("node_host_02"),
        ClusterConsensusNode("node_host_03"),
        ClusterConsensusNode("node_host_04"),
        ClusterConsensusNode("node_host_05")
    ]
    
    # 2. Connect nodes via the simulated communication mesh
    network_mesh = ClusterCommunicationMesh(cluster_nodes)

    print("--- Initializing Storage Cluster Nodes ---")
    ClusterMetricsDashboard.output_cluster_matrix(cluster_nodes)

    # 3. Simulate an election timeout on node_host_01
    print("\n[ELECTION-START] node_host_01 timed out. Initiating election loop...")
    candidate_node = cluster_nodes[0]
    candidate_node.consensus_state.transition_to_candidate()

    # Request votes across the cluster network mesh
    total_votes = network_mesh.broadcast_election_votes(candidate_node)
    majority_threshold = (len(cluster_nodes) // 2) + 1
    
    print(f"[ELECTION-POLL] Votes Received: {total_votes}/{len(cluster_nodes)} (Majority Quorum Needed: {majority_threshold})")
    
    if total_votes >= majority_threshold:
        candidate_node.consensus_state.transition_to_leader()
        # Align peers with the winning leader's term
        for node in cluster_nodes:
            if node.node_id != candidate_node.node_id:
                node.consensus_state.current_term = candidate_node.consensus_state.current_term

    ClusterMetricsDashboard.output_cluster_matrix(cluster_nodes)

    # 4. Process data writes via the elected cluster leader node
    leader_node = cluster_nodes[0]
    if leader_node.consensus_state.current_role == "Leader":
        print("\n[WRITE-START] Ingesting client request: SET counter=100...")
        write_success = network_mesh.replicate_leader_command(leader_node, "SET counter=100")
        print(f"Log Consensus Reached and Committed Globally? -> {write_success}")

        print("\n[WRITE-START] Ingesting client request: SET system_auth=true...")
        write_success_2 = network_mesh.replicate_leader_command(leader_node, "SET system_auth=true")
        print(f"Log Consensus Reached and Committed Globally? -> {write_success_2}")

    # Show final cluster states proving logs replicated and committed evenly everywhere
    ClusterMetricsDashboard.output_cluster_matrix(cluster_nodes)

if __name__ == "__main__":
    main()