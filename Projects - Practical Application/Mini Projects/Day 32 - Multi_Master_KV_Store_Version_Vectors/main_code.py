"""
System: Highly-Available Multi-Master Key-Value Store Engine
Description: A production-grade decentralized storage node cluster featuring version vector 
             tracking, multi-master write operations, and programmatic sibling client resolution.
Lead Engineer: Syed Saad Bin Irfan
"""

import logging
from typing import Dict, List, Tuple, Any, set

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)s] (MultiMaster-KV) %(message)s')

class MultiMasterStorageNode:
    """An independent storage node that accepts client writes and maintains version histories."""
    
    def __init__(self, node_id: str) -> None:
        self.node_id: str = node_id
        # Internal partition store: maps DataKey -> Dict[SerializedVectorString, TargetValue]
        self.database_partition: Dict[str, Dict[str, str]] = {}
        # Tracks the node's local execution vector clock counter
        self.local_version_vector: Dict[str, int] = {node_id: 0}

    def direct_client_write(self, key: str, value: str, client_ctx_vector: Dict[str, int]) -> Dict[str, int]:
        """Processes an incoming write from a client, increments the local clock, and stores the update."""
        # Merge client context to ensure causality is preserved
        for k, v in client_ctx_vector.items():
            self.local_version_vector[k] = max(self.local_version_vector.get(k, 0), v)
            
        self.local_version_vector[self.node_id] += 1
        current_write_vector = dict(self.local_version_vector)
        serialized_vector = str(sorted(current_write_vector.items()))
        
        if key not in self.database_partition:
            self.database_partition[key] = {}
            
        # Clean up any old versions that this new write safely supersedes
        active_versions = list(self.database_partition[key].keys())
        for existing_str in active_versions:
            existing_dict = dict(eval(existing_str))
            
            # Evaluate if the new write dominates the existing record
            new_is_newer = True
            for n in set(current_write_vector.keys()).union(existing_dict.keys()):
                if current_write_vector.get(n, 0) < existing_dict.get(n, 0):
                    new_is_newer = False
                    break
            if new_is_newer:
                del self.database_partition[key][existing_str]

        self.database_partition[key][serialized_vector] = value
        logging.info(f"[{self.node_id}] Write Accepted. Key: '{key}' | Assigned Vector: {current_write_vector}")
        return current_write_vector

    def fetch_data_with_vectors(self, key: str) -> Tuple[List[str], Dict[str, int]]:
        """Returns all active values (including siblings) and the merged structural clock state."""
        if key not in self.database_partition or not self.database_partition[key]:
            return ([], dict(self.local_version_vector))
            
        values = list(self.database_partition[key].values())
        
        # Build a consolidated vector clock that encompasses all sibling variants
        consolidated_vector: Dict[str, int] = {}
        for serialized_str in self.database_partition[key].keys():
            v_dict = dict(eval(serialized_str))
            for k, v in v_dict.items():
                consolidated_vector[k] = max(consolidated_vector.get(k, 0), v)
                
        return (values, consolidated_vector)

    def background_reconciliation_sync(self, key: str, external_history: Dict[str, str]) -> None:
        """Merges values from another node during background anti-entropy sync processing."""
        if key not in self.database_partition:
            self.database_partition[key] = {}
            
        for ext_vec_str, ext_val in external_history.items():
            self.database_partition[key][ext_vec_str] = ext_val


if __name__ == "__main__":
    print("\n=== STARTING MULTI-MASTER DISTRIBUTED STORAGE SYSTEM ===\n")
    
    # Initialize two storage nodes representing separated data centers
    datacenter_east = MultiMasterStorageNode("dc-east")
    datacenter_west = MultiMasterStorageNode("dc-west")
    
    # Client writes initial configuration data to dc-east
    print("[CLIENT-TRANSACTION] Writing baseline parameters to East DataCenter...")
    v_base = datacenter_east.direct_client_write("app_config_key", "MaxConnections=100", {})
    
    # Sync the initial write to the West cluster node
    datacenter_west.background_reconciliation_sync("app_config_key", datacenter_east.database_partition["app_config_key"])
    
    # Simulate a network partition where clients update both nodes concurrently
    print("\n[PARTITION-EVENT] Concurrent configuration writes hit both isolated nodes simultaneously...")
    v_east_inc = datacenter_east.direct_client_write("app_config_key", "MaxConnections=150", v_base)
    v_west_inc = datacenter_west.direct_client_write("app_config_key", "MaxConnections=200", v_base)
    
    # Heal partition and sync states between clusters
    print("\n[ANTI-ENTROPY-SYNC] Reconnecting datacenters and merging version records...")
    datacenter_east.background_reconciliation_sync("app_config_key", datacenter_west.database_partition["app_config_key"])
    
    # Read the data back from the East node to view conflict states
    sibling_variants, merged_clock = datacenter_east.fetch_data_with_vectors("app_config_key")
    print(f"\n[READ-RESOLVE] Sibling records detected on East node: {sibling_variants}")
    print(f"[READ-RESOLVE] Merged Version Vector Context: {merged_clock}")
    
    # Resolve the conflict with a clean overwrite
    print("\n[CLIENT-RESOLUTION] Client reconciles siblings and saves the canonical version...")
    datacenter_east.direct_client_write("app_config_key", "MaxConnections=200;ResolvedViaClient", merged_clock)
    
    print("\n=== SYSTEM SHUTDOWN: MULTI-MASTER ENGINE EXITED ===")