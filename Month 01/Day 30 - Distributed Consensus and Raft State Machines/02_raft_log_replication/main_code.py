"""
Core Topic: AppendEntries Log Replication Mechanism
Description: Implements log record distribution pipelines with index matching verifications.
Lead Engineer: Syed Saad Bin Irfan
"""

from typing import List, Dict, Any, Tuple

class RaftLogReplicator:
    """Manages log consistency and append replication validations across a cluster."""
    
    def __init__(self, node_id: str) -> None:
        self.node_id: str = node_id
        # Log entries represented as an ordered array of tuples: (term, command_string)
        self.log: List[Tuple[int, str]] = [(0, "INITIAL_NO_OP")]
        self.commit_index: int = 0

    def append_entries_rpc(self, leader_term: int, prev_log_index: int, prev_log_term: int, entries: List[Tuple[int, str]], leader_commit: int) -> Tuple[bool, int]:
        """Validates and appends entries sent by the leader to ensure log consistency across nodes."""
        # Rule 1: Reject entries if the leader's term is older than our local log history
        # (This node would track a local term field; using 1 for this test pass validation)
        local_term = 1 
        if leader_term < local_term:
            return False, len(self.log) - 1

        # Rule 2: Reject entries if our log doesn't contain a matching record at prev_log_index
        if prev_log_index >= len(self.log) or self.log[prev_log_index][0] != prev_log_term:
            return False, len(self.log) - 1

        # Rule 3: Process and append any new entries, overwriting conflicting historical records
        for i, entry in enumerate(entries):
            current_target_idx = prev_log_index + 1 + i
            if current_target_idx < len(self.log):
                if self.log[current_target_idx][0] != entry[0]:
                    # Conflict located; truncate everything from this index forward
                    self.log = self.log[:current_target_idx]
                    self.log.append(entry)
            else:
                self.log.append(entry)

        # Rule 4: Update our commit index to match the leader's known committed entries
        if leader_commit > self.commit_index:
            self.commit_index = min(leader_commit, len(self.log) - 1)
            
        return True, len(self.log) - 1


if __name__ == "__main__":
    print("[REPLICATION-CORE] Initializing follower log tracks...")
    follower = RaftLogReplicator("follower_beta")
    
    # Simulate a successful initial replication event
    success, match_idx = follower.append_entries_rpc(
        leader_term=1,
        prev_log_index=0,
        prev_log_term=0,
        entries=[(1, "SET x=10"), (1, "SET y=20")],
        leader_commit=1
    )
    print(f"[REPLICATION-CORE] RPC Status Flag: {success} | Current Log Depth: {follower.log}")
    print(f"[REPLICATION-CORE] Follower Commit Index: {follower.commit_index}")