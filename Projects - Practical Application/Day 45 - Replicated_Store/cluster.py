"""
Component: Network Communication Simulation Mesh
Description: Models RPC network delivery to simulate cluster voting and log replication.
Lead Engineer: Syed Saad Bin Irfan
"""

from typing import List
from node import ClusterConsensusNode

class ClusterCommunicationMesh:
    """Simulates a network cluster, routing RPC voting and replication requests among nodes."""
    
    def __init__(self, nodes: List[ClusterConsensusNode]) -> None:
        self.nodes = nodes

    def broadcast_election_votes(self, candidate_node: ClusterConsensusNode) -> int:
        """Gathers votes from peer nodes to decide if a candidate wins election."""
        votes_granted = 1  # Start with the candidate's self-vote
        candidate_state = candidate_node.consensus_state
        
        last_log_idx = len(candidate_node.storage.entries_log) - 1
        last_log_trm = candidate_node.storage.entries_log[last_log_idx]["term"] if last_log_idx >= 0 else 0

        for peer in self.nodes:
            if peer.node_id == candidate_node.node_id:
                continue
                
            vote_approved = peer.process_vote_request(
                candidate_id=candidate_node.node_id,
                candidate_term=candidate_state.current_term,
                last_log_index=last_log_idx,
                last_log_term=last_log_trm
            )
            if vote_approved:
                votes_granted += 1

        return votes_granted

    def replicate_leader_command(self, leader_node: ClusterConsensusNode, command: str) -> bool:
        """Appends a command to the leader's log and replicates it to all followers."""
        leader_state = leader_node.consensus_state
        
        # 1. Append command locally on the leader node
        new_index = leader_node.storage.append_entry(leader_state.current_term, command)
        replication_success_count = 1  # Count the leader's local write
        
        # 2. Replicate entry to peer followers
        packaged_entry = [{"term": leader_state.current_term, "command": command}]
        
        for peer in self.nodes:
            if peer.node_id == leader_node.node_id:
                continue
                
            success = peer.process_append_entries(
                leader_id=leader_node.node_id,
                leader_term=leader_state.current_term,
                entries=packaged_entry,
                leader_commit=leader_state.commit_index
            )
            if success:
                replication_success_count += 1

        # 3. If a majority of nodes append the entry, commit it on the leader
        majority_threshold = (len(self.nodes) // 2) + 1
        if replication_success_count >= majority_threshold:
            leader_state.commit_index = new_index
            leader_node.storage.apply_to_state_machine(new_index)
            return True
            
        return False