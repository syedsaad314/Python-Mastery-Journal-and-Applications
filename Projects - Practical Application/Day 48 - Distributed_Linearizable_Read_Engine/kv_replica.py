# Lead Engineer: Syed Saad Bin Irfan
"""
Portfolio Layer: Volatile Memory Key-Value Store Replica Replicators
"""
from typing import Dict, Any

class KVReplicaStore:
    def __init__(self) -> None:
        self.storage_map: Dict[str, str] = {
            "developer_profile": "Saad Bin Irfan - BSSE Student",
            "system_tier": "Production-Alpha",
            "cluster_health": "Optimal"
        }

    def execute_local_read(self, key: str) -> str:
        return self.storage_map.get(key, "KEY_NOT_FOUND")

    def execute_local_mutation(self, parsed_cmd: str) -> str:
        # Simple parser layout handler matching structural layout format tokens "SET k=v"
        if parsed_cmd.startswith("SET "):
            raw_kv = parsed_cmd[4:]
            key, val = raw_kv.split("=", 1)
            self.storage_map[key] = val
            return f"MUTATION_SUCCESS: {key} updated"
        return "ERROR: INVALID_COMMAND"