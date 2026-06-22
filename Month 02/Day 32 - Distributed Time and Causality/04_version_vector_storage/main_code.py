"""
Core Topic: Version Vector Database Partition Partitioning
Description: Storage tracking structural layer detecting write conflicts via system version vectors.
Lead Engineer: Syed Saad Bin Irfan
"""

from typing import Dict, Any, Tuple, Optional

class VersionedStorageCell:
    """Manages data storage for a specific key, tracking its update history with version vectors."""
    
    def __init__(self) -> __name__:
        # Maps a string representation of a version vector to its stored value
        self.version_history: Dict[str, str] = {}

    def extract_latest_states(self) -> Dict[str, str]:
        return dict(self.version_history)

    def force_override_write(self, canonical_vector: Dict[str, int], target_value: str) -> None:
        """Saves a value and overwrites the history once a conflict is resolved."""
        serialized_key = str(sorted(canonical_vector.items()))
        self.version_history = {serialized_key: target_value}

    def stage_write(self, request_vector: Dict[str, int], incoming_value: str) -> str:
        """Saves an incoming update or flags a conflict if it can't be automatically merged."""
        if not self.version_history:
            serialized_key = str(sorted(request_vector.items()))
            self.version_history[serialized_key] = incoming_value
            return "SUCCESS_NEW_ENTRY"

        current_history_snapshots = list(self.version_history.keys())
        has_conflict = False
        superseded_keys = []

        for historical_str in current_history_snapshots:
            # Parse the serialized string back into a dictionary
            historical_dict = dict(eval(historical_str))
            
            # Evaluate relationship between existing data and the incoming write
            all_nodes = set(request_vector.keys()).union(historical_dict.keys())
            req_dominated = False
            hist_dominated = False
            
            for n in all_nodes:
                v_req = request_vector.get(n, 0)
                v_hist = historical_dict.get(n, 0)
                if v_req < v_hist:
                    req_dominated = True
                if v_hist < v_req:
                    hist_dominated = True
                    
            if req_dominated and not hist_dominated:
                # The incoming write is older than our existing data; reject or ignore it
                return "REJECTED_STALE_WRITE"
            elif hist_dominated and not req_dominated:
                # The incoming write is newer; track the old record to clean it up
                superseded_keys.append(historical_str)
            elif not req_dominated and not hist_dominated:
                # Updates happened independently; a conflict must be flagged
                has_conflict = True

        if has_conflict:
            serialized_key = str(sorted(request_vector.items()))
            self.version_history[serialized_key] = incoming_value
            return "CONFLICT_DETECTED_SIBLINGS_CREATED"

        # Clean up old versions if the new write cleanly replaces them
        for old_key in superseded_keys:
            del self.version_history[old_key]
            
        new_key = str(sorted(request_vector.items()))
        self.version_history[new_key] = incoming_value
        return "SUCCESS_UPDATED"


if __name__ == "__main__":
    storage_cell = VersionedStorageCell()
    
    # Establish a baseline write
    storage_cell.stage_write({"replica_a": 1}, "Initial Value String")
    
    # Simulate concurrent updates sent to separate replicas
    status_1 = storage_cell.stage_write({"replica_a": 1, "replica_b": 1}, "Variant-B")
    status_2 = storage_cell.stage_write({"replica_a": 1, "replica_c": 1}, "Variant-C")
    
    print(f"[STORAGE] Staging write 1 status: {status_1}")
    print(f"[STORAGE] Staging write 2 status: {status_2}")
    print(f"[STORAGE] Active values held in conflict storage: {list(storage_cell.extract_latest_states().values())}")