"""
Core Topic: Node Churn Data Migration Analyzer
Description: Measures data migration rates during node add/remove operations to prove ring efficiency.
Lead Engineer: Syed Saad Bin Irfan
"""

from typing import List, Dict, Tuple
from main_code import VirtualNodeHashRing # Reuses logic structure from previous module safely

def analyze_churn_migration() -> None:
    """Simulates a cluster scale-out event and calculates the percentage of data keys that need to migrate."""
    initial_nodes = ["node_1", "node_2", "node_3", "node_4"]
    ring = VirtualNodeHashRing(initial_nodes, vnode_count=100)
    
    # Map out the initial location of 2000 data keys
    initial_allocations: Dict[str, str] = {}
    for i in range(2000):
        key = f"cache_key_string_{i}"
        node = ring.get_node(key)
        if node:
            initial_allocations[key] = node

    # Simulate scaling out the cluster by adding a fifth server node
    print("[CHURN-ANALYZER] Scaling cluster out: Adding 'node_5' into active topology...")
    ring.add_node("node_5")
    
    # Audit allocations after the cluster modification
    migrated_keys_count = 0
    for key, previous_node in initial_allocations.items():
        new_node = ring.get_node(key)
        if new_node != previous_node:
            migrated_keys_count += 1
            
    migration_percentage = (migrated_keys_count / len(initial_allocations)) * 100
    print(f"[CHURN-ANALYZER] Migration Audit: {migrated_keys_count}/2000 keys reassigned.")
    print(f"[CHURN-ANALYZER] Total Migrated Overhead: {migration_percentage:.2f}% (Expected near ~20%)")


if __name__ == "__main__":
    analyze_churn_migration()