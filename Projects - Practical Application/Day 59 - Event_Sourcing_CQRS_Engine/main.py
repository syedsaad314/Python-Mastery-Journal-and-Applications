# Lead Engineer: Syed Saad Bin Irfan
"""
Portfolio Layer: Master Operational Verification Harness for Event Sourcing & CQRS
"""
import asyncio
from store import EventStoreEngine
from projections import MaterializedAccountViewProjection

class AccountAggregateService:
    """Combines Command Validation, Reconstitution, and Snapshots"""
    def __init__(self, account_id: str, store: EventStoreEngine) -> None:
        self.account_id = account_id
        self.store = store
        self.balance = 0.0
        self.status = "UNINITIALIZED"
        self.version = 0

    def load_and_reconstitute(self) -> None:
        # 1. Load the nearest available snapshot checkpoint
        snapshot_ver, snapshot_state = self.store.load_snapshot(self.account_id)
        if snapshot_ver > 0:
            self.balance = snapshot_state["balance"]
            self.status = snapshot_state["status"]
            self.version = snapshot_ver
            
        # 2. Replay only the events appended AFTER that snapshot version
        trailing_events = self.store.read_stream_mutations(self.account_id, starting_version=snapshot_ver)
        for evt in trailing_events:
            self.apply_mutation(evt.event_type, evt.payload)
            self.version = evt.version

    def apply_mutation(self, event_type: str, payload: dict) -> None:
        if event_type == "LEDGER_OPENED":
            self.balance = payload["initial_deposit"]
            self.status = "ACTIVE"
        elif event_type == "FUNDS_CREDITED":
            self.balance += payload["amount"]
        elif event_type == "FUNDS_DEBITED":
            self.balance -= payload["amount"]

    def execute_credit(self, amount: float) -> dict:
        if amount <= 0:
            raise ValueError("Credit amount must be positive.")
        print(f"[COMMAND VALIDATED] Safe Credit: +${amount}")
        return {"type": "FUNDS_CREDITED", "payload": {"amount": amount}}

    def execute_debit(self, amount: float) -> dict:
        if amount <= 0:
            raise ValueError("Debit amount must be positive.")
        if self.balance < amount:
            raise ValueError(f"Insufficient funds! Balance: ${self.balance}, Request: ${amount}")
        print(f"[COMMAND VALIDATED] Safe Debit: -${amount}")
        return {"type": "FUNDS_DEBITED", "payload": {"amount": amount}}


async def master_verification_harness() -> None:
    print("=========================================================================")
    print("       RUNNING ACTIVATION TRACK: EVENT SOURCING & CQRS ENGINE           ")
    print("=========================================================================")

    # Initialize core system components
    storage_facility = EventStoreEngine()
    read_projection_hub = MaterializedAccountViewProjection()

    # -------------------------------------------------------------------------
    # PART 1: Initialize Account & Process Valid Transaction Commands
    # -------------------------------------------------------------------------
    print("\n--- STEP 1: Initializing Streams and Appending Valid Mutations ---")
    account_token = "ACC-SAAD-2026"
    
    # Simulate initial registration workflow
    init_service = AccountAggregateService(account_token, storage_facility)
    init_service.load_and_reconstitute()
    
    events_to_store = [{"type": "LEDGER_OPENED", "payload": {"owner": "Syad Saad Bin Irfan", "initial_deposit": 1500.0}}]
    records = storage_facility.append_events(account_token, current_version=0, new_events=events_to_store)
    
    # Keep the read-optimized projection view synchronized
    for r in records: read_projection_hub.consume(r)

    # Re-load the state model to process subsequent transaction steps
    active_service = AccountAggregateService(account_token, storage_facility)
    active_service.load_and_reconstitute()
    
    # Process valid transaction modifications
    evt1 = active_service.execute_credit(500.0)
    evt2 = active_service.execute_debit(300.0)
    
    new_records = storage_facility.append_events(account_token, current_version=active_service.version, new_events=[evt1, evt2])
    for r in new_records: read_projection_hub.consume(r)

    # -------------------------------------------------------------------------
    # PART 2: Trigger Snapshot Checkpointing & Process Invariant Failures
    # -------------------------------------------------------------------------
    print("\n--- STEP 2: Saving Snapshot and Enforcing Business Rule Invariants ---")
    active_service.load_and_reconstitute()
    
    # Save a snapshot checkpoint at the current version to optimize future lookups
    storage_facility.save_snapshot(account_token, active_service.version, {"balance": active_service.balance, "status": active_service.status})
    print(f"[SNAPSHOT CHECKPOINT] Saved state at version {active_service.version}. Balance: ${active_service.balance}")

    # Verify that business rule guards catch illegal commands
    try:
        active_service.execute_debit(5000.0) # This should fail because it exceeds the balance
    except ValueError as err:
        print(f"[INVARIANT BLOCKED] ❌ Blocked illegal command: {err}")

    # -------------------------------------------------------------------------
    # PART 3: Verify CQRS Read Views and Reconstitution Performance
    # -------------------------------------------------------------------------
    print("\n--- STEP 3: Verifying Read-Optimized Views and State Reconstitution ---")
    
    final_tester = AccountAggregateService(account_token, storage_facility)
    final_tester.load_and_reconstitute()
    
    print("\n[SYSTEM VERIFICATION REPORT]")
    print(f"Write Model Reconstituted Balance : ${final_tester.balance}")
    print(f"Write Model Stream Version Match  : Version {final_tester.version}")
    print(f"CQRS Read Dashboard Index Output  : {read_projection_hub.dashboard_index[account_token]}")

if __name__ == "__main__":
    asyncio.run(master_verification_harness())