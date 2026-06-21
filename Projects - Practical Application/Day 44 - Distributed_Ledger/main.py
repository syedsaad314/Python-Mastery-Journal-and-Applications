"""
System: Core Distributed Financial Ledger Entry Point
Description: Sets up participant databases, initializes coordinators, and runs transaction profiles.
Lead Engineer: Syed Saad Bin Irfan
"""

from transaction import LedgerTransaction
from ledger import LocalLedgerAccountSpace
from participant import ParticipantCohortNode
from coordinator import TransactionCommitCoordinator
from metrics import LedgerMetricsDashboard

def main() -> None:
    # 1. Initialize local ledger databases for independent database instances
    ledger_space_a = LocalLedgerAccountSpace("primary_vault_node_a")
    ledger_space_b = LocalLedgerAccountSpace("secondary_vault_node_b")

    # Set up starting accounts and token balances across nodes
    ledger_space_a.configure_balance_profile("saad_irfan_01", 5000.0)
    ledger_space_b.configure_balance_profile("fabha_iqbal_02", 1200.0)

    # 2. Wrap ledger spaces inside network participant components
    node_a = ParticipantCohortNode("node_host_a", ledger_space_a)
    node_b = ParticipantCohortNode("node_host_b", ledger_space_b)
    cluster_nodes = [node_a, node_b]

    # 3. Create the central transaction coordinator
    coordinator = TransactionCommitCoordinator(cluster_nodes)

    # Show the initial system balance matrix
    print("--- Booting Ledger Cluster States ---")
    LedgerMetricsDashboard.output_current_balances(cluster_nodes)

    # Case Profile A: Process a valid financial transaction
    print("\n[TRANSACTION-START] Attempting to transfer 1500 Tokens from saad_irfan_01 to fabha_iqbal_02...")
    tx_1 = LedgerTransaction("tx_uuid_99812", "saad_irfan_01", "fabha_iqbal_02", 1500.0)
    tx_1_outcome = coordinator.dispatch_distributed_transaction(tx_1)
    print(f"Transaction Execution Outcome Successful? -> {tx_1_outcome}")

    # Show updated balances after the successful transaction
    LedgerMetricsDashboard.output_current_balances(cluster_nodes)

    # Case Profile B: Process a transaction that fails due to insufficient funds
    print("\n[TRANSACTION-START] Re-attempting to transfer 6000 Tokens (Exceeding Limit)...")
    tx_2 = LedgerTransaction("tx_uuid_99813", "saad_irfan_01", "fabha_iqbal_02", 6000.0)
    tx_2_outcome = coordinator.dispatch_distributed_transaction(tx_2)
    print(f"Transaction Execution Outcome Successful? -> {tx_2_outcome}")

    # Show final balance states proving the failed write rolled back cleanly everywhere
    LedgerMetricsDashboard.output_current_balances(cluster_nodes)

if __name__ == "__main__":
    main()