# Lead Engineer: Syed Saad Bin Irfan
"""
Portfolio Layer: Fully Featured Log Replication Raft Protocol Node Agent
"""
from typing import List, Dict, Optional, Any
from models import LogEntry, AppendEntriesRequest, AppendEntriesResponse
from state_machine import StateMachineEngine
from network_stub import SynchronousNetworkBackplane

class RaftReplicationNode:
    def __init__(self, node_id: str, cluster_ids: List[str], network: SynchronousNetworkBackplane) -> None:
        self.node_id = node_id
        self.cluster_ids = cluster_ids
        self.network = network
        
        # State & Term Variables
        self.current_term: int = 1
        self.role: str = "FOLLOWER" # "FOLLOWER" | "LEADER"
        
        # Log Arrays & Core Consensus Pointers
        self.log: List[LogEntry] = []
        self.commit_index: int = 0
        self.state_machine = StateMachineEngine()
        
        # Leader-Specific Tracker Maps
        self.next_index: Dict[str, int] = {}
        self.match_index: Dict[str, int] = {}

    def assume_leadership(self, term: int) -> None:
        self.role = "LEADER"
        self.current_term = term
        print(f"\n[NODE-{self.node_id}] ★ Transitioned to cluster LEADER for term {self.current_term}")
        
        # Initialize tracking pointers for all cluster peers
        for peer in self.cluster_ids:
            if peer != self.node_id:
                self.next_index[peer] = len(self.log) + 1
                self.match_index[peer] = 0

    def client_write_request(self, command: Any) -> bool:
        if self.role != "LEADER":
            return False
            
        # Append entry to local log buffer first
        new_index = len(self.log) + 1
        entry = LogEntry(term=self.current_term, index=new_index, command=command)
        self.log.append(entry)
        print(f"\n[NODE-{self.node_id}] Client command appended to Leader log. Index: {new_index}")
        
        # Trigger replication round to all peers
        self.replicate_logs_to_cluster()
        return True

    def replicate_logs_to_cluster(self) -> None:
        total_cluster_nodes = len(self.cluster_ids)
        # The leader inherently counts as a match for its own log position
        self.match_index[self.node_id] = len(self.log)
        
        for peer in self.cluster_ids:
            if peer == self.node_id:
                continue
                
            success = False
            while not success:
                prev_idx = self.next_index[peer] - 1
                prev_term = self.log[prev_idx - 1].term if prev_idx > 0 else 0
                entries_to_send = self.log[prev_idx:]
                
                req = AppendEntriesRequest(
                    term=self.current_term,
                    leader_id=self.node_id,
                    prev_log_index=prev_idx,
                    prev_log_term=prev_term,
                    entries=entries_to_send,
                    leader_commit=self.commit_index
                )
                
                res = self.network.route_append_entries(peer, req)
                
                if res.success:
                    self.next_index[peer] = res.match_index + 1
                    self.match_index[peer] = res.match_index
                    success = True
                else:
                    # Log conflict detected: decrement nextIndex and retry step
                    if self.next_index[peer] > 1:
                        self.next_index[peer] -= 1
                    else:
                        break # Prevent underflow boundaries

        # Re-evaluate commit index thresholds following peer updates
        self.evaluate_and_advance_commit_index()

    def evaluate_and_advance_commit_index(self) -> None:
        all_matches = sorted(list(self.match_index.values()))
        median_idx = len(self.cluster_ids) // 2
        highest_majority_index = all_matches[median_idx]
        
        if highest_majority_index > self.commit_index:
            # Raft Safety Rule: Only commit entries from the current term directly
            if self.log[highest_majority_index - 1].term == self.current_term:
                self.commit_index = highest_majority_index
                print(f"[LEADER-CONVERGENCE] Majority verified! Advanced Commit Index -> {self.commit_index}")
                self.apply_logs_to_state_machine()

    def handle_append_entries_rpc(self, request: AppendEntriesRequest) -> AppendEntriesResponse:
        # Rule 1: Reject if the inbound term is lower than our current term
        if request.term < self.current_term:
            return AppendEntriesResponse(self.current_term, False, 0, self.node_id)
            
        if request.term > self.current_term:
            self.current_term = request.term
            self.role = "FOLLOWER"
            
        # Rule 2: Log Matching Property check
        if request.prev_log_index > 0:
            if len(self.log) < request.prev_log_index or self.log[request.prev_log_index - 1].term != request.prev_log_term:
                print(f"[NODE-{self.node_id}] Log mismatch at index {request.prev_log_index}. Rejecting update.")
                return AppendEntriesResponse(self.current_term, False, len(self.log), self.node_id)

        # Rule 3 & 4: Append new entries and truncate conflicts
        for entry in request.entries:
            idx_pos = entry.index - 1
            if idx_pos < len(self.log):
                if self.log[idx_pos].term != entry.term:
                    print(f"[NODE-{self.node_id}] Overwriting conflicting history from index {entry.index}")
                    self.log = self.log[:idx_pos]
                    self.log.append(entry)
            else:
                self.log.append(entry)

        # Rule 5: Update the local commit index to match the leader's progress
        if request.leader_commit > self.commit_index:
            self.commit_index = min(request.leader_commit, len(self.log))
            print(f"[NODE-{self.node_id}] Advanced Local Commit Index -> {self.commit_index}")
            self.apply_logs_to_state_machine()

        return AppendEntriesResponse(self.current_term, True, len(self.log), self.node_id)

    def apply_logs_to_state_machine(self) -> None:
        self.state_machine.apply_committed_logs_sequence(self.log, self.commit_index)

# Inject matching helper method directly to complete the class implementation cleanly
def apply_committed_logs_sequence(self, log_history: List[LogEntry], commit_idx: int) -> None:
    while self.last_applied_index < commit_idx:
        target_entry = log_history[self.last_applied_index]
        self.apply_command(target_entry.index, target_entry.command)

StateMachineEngine.apply_committed_logs_sequence = apply_committed_logs_sequence