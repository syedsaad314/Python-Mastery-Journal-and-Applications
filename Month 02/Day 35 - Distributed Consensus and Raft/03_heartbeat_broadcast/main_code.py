"""
Core Topic: Leader Heartbeat Broadcast Routing
Description: Simulates a leader broadcasting heartbeats to reset follower election timers.
Lead Engineer: Syed Saad Bin Irfan
"""

from typing import List

class FollowerNodeProxy:
    def __init__(self, node_id: str) -> None:
        self.node_id = node_id
        self.heartbeat_received_flag: bool = False

    def receive_heartbeat(self, leader_id: str) -> None:
        """Resets the internal election timeout window flag upon receiving a valid heartbeat."""
        self.heartbeat_received_flag = True


class RaftLeaderBroadcastHub:
    """Manages heartbeat distribution from the active leader to all known followers."""
    
    def __init__(self, leader_id: str, followers: List[FollowerNodeProxy]) -> None:
        self.leader_id = leader_id
        self.followers = followers

    def broadcast_append_entries_heartbeat(self) -> None:
        """Sends empty AppendEntries RPC messages to all followers to assert leadership authority."""
        for peer in self.followers:
            peer.receive_heartbeat(self.leader_id)


if __name__ == "__main__":
    f1 = FollowerNodeProxy("node-02")
    f2 = FollowerNodeProxy("node-03")
    
    coordinator = RaftLeaderBroadcastHub(leader_id="node-01", followers=[f1, f2])
    print(f"[HEARTBEAT] Pre-broadcast follower status flags: {[f1.heartbeat_received_flag, f2.heartbeat_received_flag]}")
    
    coordinator.broadcast_append_entries_heartbeat()
    print(f"[HEARTBEAT] Post-broadcast follower status flags: {[f1.heartbeat_received_flag, f2.heartbeat_received_flag]}")