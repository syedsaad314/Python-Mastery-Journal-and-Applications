# Lead Engineer: Syed Saad Bin Irfan
"""
Portfolio Layer: Struct Definitions and Network Data Entities
"""
from typing import NamedTuple, List

class NodeConfig(NamedTuple):
    node_id: str
    max_capacity_weight: int
    vnode_count: int

class RingLookupResult(NamedTuple):
    key: str
    primary_node: str
    replica_nodes: List[str]
    routing_strategy: str