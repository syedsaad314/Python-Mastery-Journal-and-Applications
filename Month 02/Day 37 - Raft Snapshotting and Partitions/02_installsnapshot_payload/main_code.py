"""
Core Topic: InstallSnapshot RPC Data Structural Layout
Description: Defines the structured network schema required to transmit heavy snapshots to lagging peers.
Lead Engineer: Syed Saad Bin Irfan
"""

from typing import Dict, Any

class InstallSnapshotPayloadBuilder:
    """Constructs explicit network frames for Raft InstallSnapshot RPC messages."""
    
    @staticmethod
    def build_rpc_packet(
        leader_term: int,
        leader_id: str,
        last_included_index: int,
        last_included_term: int,
        raw_snapshot_data: bytes
    ) -> Dict[str, Any]:
        return {
            "term": leader_term,
            "leader_id": leader_id,
            "last_included_index": last_included_index,
            "last_included_term": last_included_term,
            "data_bytes": raw_snapshot_data
        }


if __name__ == "__main__":
    mock_snapshot = b'{"data_store_state": {"balance": 25000}}'
    
    rpc_packet = InstallSnapshotPayloadBuilder.build_rpc_packet(
        leader_term=4,
        leader_id="master-node-01",
        last_included_index=120,
        last_included_term=3,
        raw_snapshot_data=mock_snapshot
    )
    
    print(f"[RPC-PAYLOAD] Fully structured InstallSnapshot RPC Frame packet:")
    print(f" -> Term: {rpc_packet['term']} | Leader: {rpc_packet['leader_id']}")
    print(f" -> Boundary Target Index: {rpc_packet['last_included_index']} (Term {rpc_packet['last_included_term']})")