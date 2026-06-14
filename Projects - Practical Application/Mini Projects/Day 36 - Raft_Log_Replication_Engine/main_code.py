"""
System: Multi-Node Resilient Raft Log Replication Engine
Description: A high-fidelity production-grade emulator of the Raft log replication pipeline. 
             Features AppendEntries RPC distribution, automated follower consistency rollbacks, 
             match index convergence tracing, and strict consensus majority commit tracking.
Lead Engineer: Syed Saad Bin Irfan
"""

import logging
from typing import Dict, List, Tuple

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)s] (Raft-Replication) %(message)s')

class RaftFollowerNode:
    """Manages local log histories, processing validation logic and resolving conflicts with the leader."""
    
    def __init__(self, node_id: str) -> None:
        self.node_id: str = node_id
        self.log: List[Dict[str, any]] = [{"term": 0, "command": "GENESIS"}]

    def handle_append_entries(self, prev_log_index: int, prev_log_term: int, entries: List[Dict[str, any]]) -> Tuple[bool, int]:
        """Validates incoming entries against local history, resolving conflicts and updating the log."""
        # Check 1: Ensure the follower's log is long enough to contain prev_log_index
        if prev_log_index >= len(self.log):
            logging.warning(f"[{self.node_id}] Append Rejected: Gap detected. Local log length {len(self.log)} <= PrevIndex {prev_log_index}")
            return False, len(self.log)

        # Check 2: Verify the term at prev_log_index matches the leader's expectations
        if self.log[prev_log_index]["term"] != prev_log_term:
            logging.warning(f"[{self.node_id}] Append Rejected: Term mismatch at index {prev_log_index}. Expected Term {prev_log_term}, found {self.log[prev_log_index]['term']}")
            # Truncate the log to clear out the mismatched history
            self.log = self.log[:prev_log_index]
            return False, len(self.log)

        # Step 3: Append new entries, overwriting any conflicting history at overlapping indices
        for i, entry in enumerate(entries):
            current_target_idx = prev_log_index + 1 + i
            if current_target_idx < len(self.log):
                if self.log[current_target_idx]["term"] != entry["term"]:
                    logging.info(f"[{self.node_id}] Conflict resolved: Truncating mismatched history from index {current_target_idx} onwards.")
                    self.log = self.log[:current_target_idx]
                    self.log.append(entry)
            else:
                self.log.append(entry)

        return True, len(self.log)


class RaftLeaderEngine:
    """Orchestrates log replication across followers, managing tracking arrays and match pointers."""
    
    def __init__(self, leader_id: str, peers: List[RaftFollowerNode], initial_term: int) -> None:
        self.leader_id: str = leader_id
        self.peers: List[RaftFollowerNode] = peers
        self.current_term: int = initial_term
        self.log: List[Dict[str, any]] = [{"term": 0, "command": "GENESIS"}]
        self.commit_index: int = 0

        # Raft state tracking vectors for log management
        # next_index: the index of the next log entry the leader will send to that follower
        self.next_index: Dict[str, int] = {p.node_id: 1 for p in peers}
        # match_index: the highest log entry known to be replicated on that follower
        self.match_index: Dict[str, int] = {p.node_id: 0 for p in peers}

    def client_write_command(self, command: str) -> None:
        """Appends a new mutation to the leader's local log and triggers a cluster replication loop."""
        entry = {"term": self.current_term, "command": command}
        self.log.append(entry)
        new_entry_index = len(self.log) - 1
        logging.info(f"[LEADER] Client command appended at index {new_entry_index}: '{command}'")
        self.broadcast_replication_payloads()

    def broadcast_replication_payloads(self) -> None:
        """Dispatches AppendEntries RPC payloads to all peers, adjusting pointers dynamically based on responses."""
        cluster_size = len(self.peers) + 1
        majority_target = (cluster_size // 2) + 1

        for peer in self.peers:
            p_id = peer.node_id
            
            # Replicate entries from next_index onwards
            p_next = self.next_index[p_id]
            staged_entries = self.log[p_next:]
            
            prev_idx = p_next - 1
            prev_trm = self.log[prev_idx]["term"]

            # Issue the simulated network RPC call to the follower
            success, response_val = peer.handle_append_entries(
                prev_log_index=prev_idx,
                prev_log_term=prev_trm,
                entries=staged_entries
            )

            if success:
                # Update tracking indices on success
                self.match_index[p_id] = prev_idx + len(staged_entries)
                self.next_index[p_id] = self.match_index[p_id] + 1
            else:
                # Step back next_index on rejection to locate where the logs match up
                logging.info(f"[LEADER] Rejection received from follower '{p_id}'. Retrying with nextIndex decremented to {max(1, p_next - 1)}.")
                self.next_index[p_id] = max(1, p_next - 1)

        # Evaluate consensus commit boundaries across the cluster
        self._evaluate_consensus_commit_line(majority_target)

    def _evaluate_consensus_commit_line(self, majority_threshold: int) -> None:
        """Finds the highest index replicated to a majority and updates the commit line."""
        all_matches = sorted(list(self.match_index.values()) + [len(self.log) - 1])
        mid_index = len(all_matches) // 2
        highest_majority_idx = all_matches[mid_index]

        # Raft Safety Guard: Leaders only commit entries from their current term directly
        if highest_majority_idx > self.commit_index:
            if self.log[highest_majority_idx]["term"] == self.current_term:
                self.commit_index = highest_majority_idx
                logging.info(f"[LEADER-CONSENSUS] Quorum reached! Cluster commit index line advanced to: {self.commit_index}")


if __name__ == "__main__":
    print("\n=== STARTING MULTI-NODE RAFT LOG REPLICATION ENGINE ===\n")
    
    # Set up cluster nodes
    follower_b = RaftFollowerNode("node-B")
    follower_c = RaftFollowerNode("node-C")
    
    # Simulate an out-of-sync cluster state (e.g., node-C was isolated and has a stale history)
    follower_c.log.append({"term": 1, "command": "STALE-CONFLICT-DATA"})
    
    cluster_leader = RaftLeaderEngine("node-A-leader", peers=[follower_b, follower_c], initial_term=2)
    
    # Sync structural index tracking arrays for the lagging follower
    cluster_leader.next_index["node-C"] = 2

    # Scenario A: Append mutations and drive convergence across the cluster
    cluster_leader.client_write_command("SET profile_id='saad_007'")
    
    # Retry replication loop to catch up the lagging node after resolving the conflict
    print("\n[RETRY-LOOP] Broadcasting updates to reconcile conflicting histories...")
    cluster_leader.broadcast_replication_payloads()
    
    print(f"\n[POST-SYNC] Follower B log trace: {follower_b.log}")
    print(f"[POST-SYNC] Follower C log trace: {follower_c.log}")
    print(f"[POST-SYNC] Leader commit index state: {cluster_leader.commit_index}")
    
    print("\n=== SYSTEM SHUTDOWN: REPLICATION CONTAINER DISCONNECTED ===")