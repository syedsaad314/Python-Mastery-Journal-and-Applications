# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: AppendEntries Heartbeats
Description: Constructs leader heartbeat messages that maintain authority 
             and suppress follower election timeouts across the cluster.
"""
from typing import Dict, Any

class HeartbeatGenerator:
    def __init__(self, leader_id: str, current_term: int) -> None:
        self.leader_id = leader_id
        self.current_term = current_term

    def generate_heartbeat_payload(self) -> Dict[str, Any]:
        return {
            "term": self.current_term,
            "leader_id": self.leader_id,
            "entries": [] # Empty entry list flags message as a passive heartbeat
        }

if __name__ == "__main__":
    generator = HeartbeatGenerator("master_host", 4)
    payload = generator.generate_heartbeat_payload()
    assert len(payload["entries"]) == 0
    assert payload["term"] == 4