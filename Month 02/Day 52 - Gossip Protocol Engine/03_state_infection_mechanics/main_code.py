# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: State Infection Mechanics
Description: Overwrites older local membership details with updated, 
             higher-value heartbeat details received from peer nodes.
"""
from typing import Dict, Any

class StateInfectionEngine:
    @staticmethod
    def infect_local_table(local_table: Dict[str, Dict[str, Any]], remote_table: Dict[str, Dict[str, Any]]) -> None:
        for node_id, remote_meta in remote_table.items():
            if node_id not in local_table:
                local_table[node_id] = remote_meta.copy()
            else:
                if remote_meta["heartbeat"] > local_table[node_id]["heartbeat"]:
                    local_table[node_id]["heartbeat"] = remote_meta["heartbeat"]
                    local_table[node_id]["status"] = remote_meta["status"]

if __name__ == "__main__":
    engine = StateInfectionEngine()
    local = {"node_X": {"heartbeat": 2, "status": "ALIVE"}}
    remote = {"node_X": {"heartbeat": 5, "status": "ALIVE"}, "node_Y": {"heartbeat": 1, "status": "ALIVE"}}
    engine.infect_local_table(local, remote)
    assert local["node_X"]["heartbeat"] == 5
    assert "node_Y" in local