"""
System: Concurrent Banking Transaction Engine
Description: A high-fidelity, thread-safe financial ledger executing atomic double-entry money 
             transfers with total deadlock protection via deterministic resource ordering.
Lead Engineer: Syed Saad Bin Irfan
"""

import logging
import threading
import time
from typing import Dict, List, Optional

# Setup highly professional structured tracing formats
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)s] (%(threadName)s) %(message)s')

class LedgerAccount:
    def __init__(self, account_id: str, client_name: str, starting_balance: float) -> None:
        self.account_id: str = account_id
        self.client_name: str = client_name
        self.balance: float = starting_balance
        # Internal mutex lock protecting this individual account's balance memory space
        self.lock: threading.Lock = threading.Lock()

class TransactionAuditLogger:
    def __init__(self) -> None:
        self.history_ledger: List[str] = []
        self.ledger_lock: threading.Lock = threading.Lock()

    def record_log(self, trace_entry: str) -> None:
        with self.ledger_lock:
            self.history_ledger.append(trace_entry)


class BankingTransactionEngine:
    def __init__(self) -> None:
        self.accounts_registry: Dict[str, LedgerAccount] = {}
        self.audit_logger = TransactionAuditLogger()

    def provision_account(self, account_id: str, client_name: str, initial_deposit: float) -> None:
        if account_id in self.accounts_registry:
            raise ValueError(f"Account identity collision: ID {account_id} already defined.")
        self.accounts_registry[account_id] = LedgerAccount(account_id, client_name, initial_deposit)
        logging.info(f"Provisioned Account [{account_id}] for {client_name} with balance: ${initial_deposit}")

    def execute_transfer(self, source_id: str, destination_id: str, amount: float) -> bool:
        """
        Executes a secure thread-safe double-entry ledger transfer between accounts.
        Implements total deadlock prevention through strict deterministic resource ordering.
        """
        if amount <= 0:
            logging.error("Transaction rejected: Transfer threshold allocations must be positive values.")
            return False

        src_acc: Optional[LedgerAccount] = self.accounts_registry.get(source_id)
        dest_acc: Optional[LedgerAccount] = self.accounts_registry.get(destination_id)

        if not src_acc or not dest_acc:
            logging.error("Transaction aborted: One or both assigned account records do not exist.")
            return False

        # --- DEADLOCK PREVENTION VIA DETERMINISTIC LOCK ACQUISITION ORDERING ---
        # If Thread A locks Acc1 then waits for Acc2, while Thread B locks Acc2 and waits for Acc1, a deadlock occurs.
        # Solution: Sort resource acquisition order lexicographically by ID.
        first_lock_target, second_lock_target = (src_acc, dest_acc) if src_acc.account_id < dest_acc.account_id else (dest_acc, src_acc)

        logging.info(f"Attempting secure ledger balance transfer pipeline: {source_id} -> {destination_id} (${amount})")
        
        # Acquire locks safely based on our deterministic order strategy
        with first_lock_target.lock:
            with second_lock_target.lock:
                # Validate fund availability after locks are secured to prevent double-spending
                if src_acc.balance < amount:
                    err_msg = f"Rejected: Insufficient funds in Source Account [{source_id}]. Current: ${src_acc.balance}"
                    logging.warning(err_msg)
                    self.audit_logger.record_log(err_msg)
                    return False

                # Perform the atomic atomic value adjustments
                src_acc.balance -= amount
                dest_acc.balance += amount
                
                # Commit audit trail updates
                success_msg = f"SUCCESS: Transferred ${amount} from [{source_id}] to [{destination_id}]."
                logging.info(success_msg)
                self.audit_logger.record_log(success_msg)
                return True


def simulate_high_frequency_traffic(engine: BankingTransactionEngine, src: str, dest: str, val: float) -> None:
    """Simulates high-volume background transaction requests across active accounts."""
    for _ in range(5):
        engine.execute_transfer(src, dest, val)
        time.sleep(0.01)

if __name__ == "__main__":
    print("\n=== INITIALIZING CONCURRENT BANKING TRANSACTION ENGINE ===\n")
    bank_core = BankingTransactionEngine()

    # Seed the account registry
    bank_core.provision_account("PK-SAAD-001", "Syed Saad Bin Irfan", 15000.00)
    bank_core.provision_account("PK-FABHA-002", "Fabha Iqbal", 25000.00)

    # Launch competing threads to simulate high-volume transaction traffic
    # Thread 1 transfers from Saad to Fabha, while Thread 2 concurrently transfers from Fabha to Saad
    thread_alpha = threading.Thread(target=simulate_high_frequency_traffic, args=(bank_core, "PK-SAAD-001", "PK-FABHA-002", 500.0), name="TxWorker-Alpha")
    thread_beta = threading.Thread(target=simulate_high_frequency_traffic, args=(bank_core, "PK-FABHA-002", "PK-SAAD-001", 1000.0), name="TxWorker-Beta")

    logging.info("Spinning up parallel transaction processing streams...")
    thread_alpha.start()
    thread_beta.start()

    thread_alpha.join()
    thread_beta.join()

    print("\n=== CONCURRENT DISPATCH RUN COMPLETE ===")
    print(f"Final Saad Balance Result: ${bank_core.accounts_registry['PK-SAAD-001'].balance:.2f}")
    print(f"Final Fabha Balance Result: ${bank_core.accounts_registry['PK-FABHA-002'].balance:.2f}")
    print("\nAudit Trail Summary Logs:")
    for entry in bank_core.audit_logger.history_ledger:
        print(f" > {entry}")