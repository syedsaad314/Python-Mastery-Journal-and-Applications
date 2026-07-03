# Lead Engineer: Syed Saad Bin Irfan
"""
Portfolio Layer: Invariant Structural Telemetry Models
"""
from typing import NamedTuple, Dict, Any

class PeerMetadata(NamedTuple):
    heartbeat_counter: int
    observed_status: str # 'ALIVE' or 'DEAD'

class ClusterGossipMessage(NamedTuple):
    origin_node_id: str
    payload_table: Dict[str, Any]