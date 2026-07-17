# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Command Handler Validation Engine
Description: Verifies business rule safety invariants against current state profiles 
             before generating new domain events.
"""
class AccountCommandHandler:
    @staticmethod
    def handle_withdraw_command(current_balance: float, withdraw_amount: float) -> dict:
        # Enforce business rules before modifying state
        if withdraw_amount <= 0:
            raise ValueError("Withdrawal amount must be greater than zero.")
        if current_balance < withdraw_amount:
            raise ValueError("Insufficient funds to execute this transaction.")
            
        # Return the generated event payload if rules pass
        return {"event_type": "FUNDS_WITHDRAWN", "payload": {"amount": withdraw_amount}}

if __name__ == "__main__":
    try:
        AccountCommandHandler.handle_withdraw_command(current_balance=100, withdraw_amount=250)
    except ValueError as err:
        print(f"[VALIDATION CAUGHT] Invariant successfully guarded: {err}")
        
    valid_evt = AccountCommandHandler.handle_withdraw_command(current_balance=500, withdraw_amount=150)
    assert valid_evt["event_type"] == "FUNDS_WITHDRAWN"