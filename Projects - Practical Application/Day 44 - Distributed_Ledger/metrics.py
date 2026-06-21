"""
Component: System Telemetry Monitoring Panel
Description: Formats and displays account balance tables and transaction metrics to the console.
Lead Engineer: Syed Saad Bin Irfan
"""

from tabulate import tabulate # type: ignore
from typing import List
from participant import ParticipantCohortNode

class LedgerMetricsDashboard:
    """Renders tabular performance views tracking current account balances across the system."""
    
    @staticmethod
    def output_current_balances(nodes: List[ParticipantCohortNode]) -> None:
        print("\n=======================================================")
        print("     DISTRIBUTED ACCOUNT LEDGER BALANCE MATRIX")
        print("=======================================================\n")
        
        balance_records = []
        for node in nodes:
            space = node.ledger_space
            for account_id, balance in space.account_balances.items():
                balance_records.append([node.node_identity, account_id, f"{balance} TOKENS"])
                
        print(tabulate(balance_records, headers=["Cluster Node Host", "Account Profile ID", "Active Available Balance"], tablefmt="presto"))
        print("-" * 55)