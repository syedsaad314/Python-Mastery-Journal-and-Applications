"""
Component: Cluster Participant Consensus Node
Description: Handles RequestVote checks and processes replicated log appends from the leader.
Lead Engineer: Syed Saad Bin Irfan
"""

from state import NodeConsensusState
from storage import WriteAheadLogStorage
from typing import List, Dict

class ClusterConsensusNode:
    """Processes consensus messages, votes in elections, and reconciles replicated logs."""
    
    def __init__(self, node_id: str) -> None:
        self.node_id = node_id
        self.consensus_state = NodeConsensusState(node_id)
        self.storage = WriteAheadLogStorage()

    def process_vote_request(self, candidate_id: str, candidate_term: int, last_log_index: int, last_log_term: int) -> bool:
        """Evaluates election terms and log progress to decide whether to grant a vote."""
        state = self.consensus_state
        
        # Rule 1: Step down if the candidate's term is newer
        if candidate_term > state.current_term:
            state.transition_to_follower(candidate_term)

        # Rule 2: Deny vote if candidate's term is older
        if candidate_term < state.current_term:
            return False

        # Rule 3: Deny vote if this node has already voted for a different candidate this term
        if state.voted_for is not None and state.voted_for != candidate_id:
            return False

        # Rule 4: Deny vote if candidate's log is less up-to-date than ours
        local_last_index = len(self.storage.entries_log) - 1
        local_last_term = self.storage.entries_log[local_last_index]["term"] if local_last_index >= 0 else 0

        if candidate_term < local_last_term:
            return False
        if candidate_term == local_last_term and last_log_index < local_last_index:
            return False

        # All rules pass; grant the vote
        state.voted_for = candidate_id
        return True

    def process_append_entries(self, leader_id: str, leader_term: int, entries: List[Dict[str, any]], leader_commit: int) -> bool:
        """Processes incoming log replication requests from a cluster leader."""
        state = self.consensus_state

        # Rule 1: Term validation check
        if leader_term < state.current_term:
            return False

        if leader_term > state.current_term or state.current_role == "Candidate":
            state.transition_to_follower(leader_term)

        # Rule 2: Append new log entries
        for entry in entries:
            self.storage.append_entry(entry["term"], entry["command"])

        # Rule 3: Advance the local commit index matching the leader's commits
        if leader_commit > state.commit_index:
            old_commit = state.commit_index
            state.commit_index = min(leader_commit, len(self.storage.entries_log) - 1)
            
            # Apply newly committed logs to the local state machine
            for idx in range(old_commit + 1, state.commit_index + 1):
                self.storage.apply_to_state_machine(idx)

        return True