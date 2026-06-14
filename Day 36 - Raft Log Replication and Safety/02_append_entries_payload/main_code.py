"""
Core Topic: AppendEntries RPC Data Structural Layout
Description: Serializes the structural parameters required for safe distributed log replication.
Lead Engineer: Syed Saad Bin Irfan
"""

from typing import List, Dict, Any

class AppendEntriesPayloadBuilder:
    """Constructs the explicit schema required for structural AppendEntries network requests."""
    
    @staticmethod
    def construct_rpc(
        leader_term: int,
        leader_id: str,
        prev_log_index: int,
        prev_log_term: int,
        entries_to_replicate: List[Dict[str, Any]],
        leader_commit_index: int
    ) -> Dict[str, Any]:
        return {
            "term": leader_term,
            "leader_id": leader_id,
            "prev_log_index": prev_log_index,
            "prev_log_term": prev_log_term,
            "entries": entries_to_replicate,
            "leader_commit": leader_commit_index
        }


if __name__ == "__main__":
    # Simulate a leader packaging entries for distribution
    staged_mutation = [{"term": 2, "command": "SET status='active'"}]
    
    rpc_packet = AppendEntriesPayloadBuilder.construct_rpc(
        leader_term=2,
        leader_id="node-leader-khi",
        prev_log_index=4,      # The index of the entry immediately preceding the new ones
        prev_log_term=1,       # The term of the entry immediately preceding the new ones
        entries_to_replicate=staged_mutation,
        leader_commit_index=3  # The leader's highest known committed log index
    )
    
    print(f"[RPC-PAYLOAD] Fully serialized AppendEntries object packet:\n{rpc_packet}")