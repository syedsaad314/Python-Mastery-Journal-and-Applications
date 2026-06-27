# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Data Migration Routing
Description: Flags keys that need to be relocated when a new node joins 
             the cluster ring layout.
"""
from typing import List, Dict

class DataMigrationRouter:
    @staticmethod
    def calculate_migrations(old_mappings: Dict[str, str], current_ring_lookup_func) -> List[str]:
        relocation_required = []
        for key, old_node in old_mappings.items():
            new_node = current_ring_lookup_func(key)
            if old_node != new_node:
                relocation_required.append(key)
        return relocation_required

if __name__ == "__main__":
    router = DataMigrationRouter()
    old = {"key_1": "node_A", "key_2": "node_B"}
    migrated = router.calculate_migrations(old, lambda k: "node_A" if k == "key_1" else "node_C")
    assert migrated == ["key_2"]