# Lead Engineer: Syed Saad Bin Irfan
"""
Portfolio Layer: Compaction-Aware Raft Consensus Node Agent
"""
from typing import List, Dict, Any, Optional
from models import LogEntry, AppendEntriesRequest, AppendEntriesResponse, InstallSnapshotRequest, InstallSnapshotResponse
from state_machine import StateMachineEngine
from network_stub import ClusterNetworkFabric

class RaftCompactionNode:
    def __init__(self, node_id: str, peers: List[str], network: ClusterNetworkFabric) -> None:
        self.node_id = node_id
        self.peers = peers
        self.network = network
        
        # State Variables
        self.role = "FOLLOWER"
        self.current_term = 1
        self.commit_index = 0
        
        # Log & Snapshot Fields
        self.log: List[LogEntry] = []
        self.state_machine = StateMachineEngine()
        
        self.last_included_index = 0
        self.last_included_term = 0
        
        # Leader Tracking Indexes
        self.next_index: Dict[str, int] = {}
        self.match_index: Dict[str, int] = {}

    def compact_log_buffer(self, clean_up_to_idx: int) -> None:
        if clean_up_to_idx <= self.last_included_index or clean_up_to_idx > self.commit_index:
            return

        print(f"\n[COMPACTION-NODE-{self.node_id}] Running log compaction up to index {clean_up_to_idx}...")
        
        # Locate the split entry to preserve its term context
        split_entry_idx = clean_up_to_idx - self.last_included_index - 1
        target_entry = self.log[split_entry_idx]
        
        self.last_included_term = target_entry.term
        # Discard entries up to the split point
        self.log = self.log[split_entry_idx + 1:]
        self.last_included_index = clean_up_to_idx
        
        print(f"[COMPACTION-NODE-{self.node_id}] Compaction Complete. Remaining Log Size: {len(self.log)}")

    def replicate_to_peer(self, peer_id: str) -> None:
        # Check if the peer needs entries that have already been compacted and discarded
        if self.next_index[peer_id] <= self.last_included_index:
            print(f"[LEADER] Peer '{peer_id}' nextIndex ({self.next_index[peer_id]}) is behind compacted threshold ({self.last_included_index}). Sending Snapshot.")
            
            req = InstallSnapshotRequest(
                term=self.current_term,
                leader_id=self.node_id,
                last_included_index=self.last_included_index,
                last_included_term=self.last_included_term,
                data=self.state_machine.capture_snapshot_state()
            )
            res = self.network.send_install_snapshot(peer_id, req)
            if res.success:
                self.next_index[peer_id] = self.last_included_index + 1
                self.match_index[peer_id] = self.last_included_index
            return

        # Fallback to standard AppendEntries if the logs are available
        prev_idx = self.next_index[peer_id] - 1
        prev_term = 0
        
        if prev_idx == self.last_included_index:
            prev_term = self.last_included_term
        elif prev_idx > self.last_included_index:
            local_pos = prev_idx - self.last_included_index - 1
            prev_term = self.log[local_pos].term

        local_start = prev_idx - self.last_included_index
        entries = self.log[local_start:]

        req = AppendEntriesRequest(
            term=self.current_term, leader_id=self.node_id,
            prev_log_index=prev_idx, prev_log_term=prev_term,
            entries=entries, leader_commit=self.commit_index
        )
        res = self.network.send_append_entries(peer_id, req)
        if res.success:
            self.next_index[peer_id] = res.match_index + 1
            self.match_index[peer_id] = res.match_index

    def handle_install_snapshot(self, req: InstallSnapshotRequest) -> InstallSnapshotResponse:
        if req.term < self.current_term:
            return InstallSnapshotResponse(self.current_term, self.node_id, False)

        print(f"\n[NODE-{self.node_id}] Intercepted InstallSnapshotRequest from leader '{req.leader_id}'. Processing...")
        
        # Clear out local logs; the snapshot replaces this history entirely
        self.log = []
        self.last_included_index = req.last_included_index
        self.last_included_term = req.last_included_term
        self.commit_index = req.last_included_index
        
        # Fast-forward our state machine to match the snapshot
        self.state_machine.restore_snapshot_state(req.last_included_index, req.last_included_term, req.data)
        
        return InstallSnapshotResponse(self.current_term, self.node_id, True)

    def handle_append_entries(self, req: AppendEntriesRequest) -> AppendEntriesResponse:
        if req.term < self.current_term:
            return AppendEntriesResponse(self.current_term, False, 0, self.node_id)
            
        # Process entries and advance logs safely
        for entry in req.entries:
            pos = entry.index - self.last_included_index - 1
            if pos >= 0:
                if pos < len(self.log):
                    if self.log[pos].term != entry.term:
                        self.log = self.log[:pos]
                        self.log.append(entry)
                else:
                    self.log.append(entry)

        if req.leader_commit > self.commit_index:
            self.commit_index = min(req.leader_commit, self.last_included_index + len(self.log))
            self.apply_committed_logs()

        return AppendEntriesResponse(self.current_term, True, self.last_included_index + len(self.log), self.node_id)

    def apply_committed_logs(self) -> None:
        while self.state_machine.last_applied_index < self.commit_index:
            next_to_apply = self.state_machine.last_applied_index + 1
            pos = next_to_apply - self.last_included_index - 1
            entry = self.log[pos]
            self.state_machine.apply_command(entry.index, entry.term, entry.command)