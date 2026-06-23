# Lead Engineer: Syed Saad Bin Irfan
"""
Component: Cluster Store Node Definition
Description: Tracks term counters, commit boundaries, and cluster node configurations.
"""

from storage import LocalLogStore

class ClusterStoreNode:
    def __init__(self, node_id: str, is_leader: bool = False) -> None:
        self.node_id = node_id
        self.current_term = 0
        self.is_leader = is_leader
        self.commit_index = -1
        self.storage = LocalLogStore()