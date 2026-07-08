# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: InstallSnapshot RPC Payloads
Description: Builds the network payload used by leaders to catch up followers 
             whose logs lag behind the leader's earliest available index.
"""
from typing import NamedTuple, Dict, Any

class InstallSnapshotRPC(NamedTuple):
    term: int
    leader_id: str
    last_included_index: int
    last_included_term: int
    data: Dict[str, Any]

def build_snapshot_rpc(term: int, leader: str, index: int, log_term: int, state: Dict[str, Any]) -> InstallSnapshotRPC:
    return InstallSnapshotRPC(
        term=term,
        leader_id=leader,
        last_included_index=index,
        last_included_term=log_term,
        data=state.copy()
    )

if __name__ == "__main__":
    rpc = build_snapshot_rpc(4, "leader_01", 100, 3, {"counter": 42})
    assert rpc.last_included_index == 100
    assert rpc.data["counter"] == 42