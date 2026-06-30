# Lead Engineer: Syed Saad Bin Irfan
"""
Portfolio Layer: Network Partition Simulator Harness
"""
from replica_node import MultiVersionReplicaNode
from tabulate import tabulate # type: ignore

def print_storage_matrix(title: str, nodes_list: list) -> None:
    print(f"\n--- {title} ---")
    headers = ["Node Identifier", "Stored Vault Key", "Active Sibling Versions Count", "Raw Payload Values / Clock Histories Map"]
    table_rows = []
    
    for node in nodes_list:
        for key, payloads in node.storage_vault.items():
            payload_details = []
            for p in payloads:
                payload_details.append(f"('{p.data_value}' VC: {p.vector_map})")
            table_rows.append([node.node_id, key, len(payloads), " || ".join(payload_details)])
            
    print(tabulate(table_rows, headers=headers, tablefmt="fancy_grid"))

def main() -> None:
    print("=========================================================================")
    print("      INITIALIZING RUNTIME: DISTRIBUTED CONFLICT RESOLUTION ENGINE       ")
    print("=========================================================================")

    # Setup isolated replica nodes
    node_alpha = MultiVersionReplicaNode("alpha_coordinator")
    node_beta = MultiVersionReplicaNode("beta_coordinator")

    # 1. Happy Path Causal Write Propagation
    print("\n[SCENARIO 1] Client executes baseline write on node Alpha...")
    payload_v1 = node_alpha.local_write("profile_schema", "v1_saad_base")
    
    # Sync Alpha's payload over to Beta
    node_beta.integrate_remote_payload("profile_schema", payload_v1)
    print_storage_matrix("CLUSTER STATE: SYNCED BASELINE", [node_alpha, node_beta])

    # 2. Network Split - Concurrent Divergent Writes
    print("\n[SCENARIO 2] Network partition occurs! Alpha and Beta are isolated.")
    print("Client updates Alpha to 'v2_saad_modified' and Beta to 'v2_saad_patch' concurrently...")
    
    payload_alpha_v2 = node_alpha.local_write("profile_schema", "v2_saad_modified")
    payload_beta_v2 = node_beta.local_write("profile_schema", "v2_saad_patch")
    
    print_storage_matrix("PARTITION STATE: DIVERGENT SIBLINGS IN ISOLATION", [node_alpha, node_beta])

    # 3. Heal Partition - Conflict Detection
    print("\n[SCENARIO 3] Network partition heals. Syncing payloads to detect conflicts...")
    
    # Replicate Alpha's changes over to Beta
    report_beta = node_beta.integrate_remote_payload("profile_schema", payload_alpha_v2)
    print(f"[CONFLICT-TELEMETRY] Syncing to Beta resulted in: {report_beta.action_taken}")
    print(f"-> Active multi-version siblings found on Beta: {report_beta.siblings_count}")

    # Replicate Beta's changes back to Alpha so both see the conflict
    node_alpha.integrate_remote_payload("profile_schema", payload_beta_v2)
    print_storage_matrix("RECONCILIATION STATE: CONFLICT DETECTED (SIBLINGS PRESERVED)", [node_alpha, node_beta])

    # 4. Manual Resolution and Clock Consolidation
    print("\n[SCENARIO 4] Executing manual merge to resolve conflicting branches...")
    final_merged_payload = node_beta.execute_manual_merge("profile_schema", "v3_saad_reconciled_final")
    
    # Propagate the resolved payload back to Alpha to restore absolute synchronization
    node_alpha.integrate_remote_payload("profile_schema", final_merged_payload)
    print_storage_matrix("FINAL CLEAN CLUSTER STATE: RECONCILED EVENTUAL CONSISTENCY", [node_alpha, node_beta])

if __name__ == "__main__":
    main()