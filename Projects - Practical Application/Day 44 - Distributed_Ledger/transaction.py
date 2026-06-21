"""
Component: Ledger Data Unit Model
Description: Defines core transaction structures tracking safe multi-node financial updates.
Lead Engineer: Syed Saad Bin Irfan
"""

class LedgerTransaction:
    """Stores data parameters for cross-node financial book entries."""
    
    def __init__(self, tx_id: str, sender: str, receiver: str, token_amount: float) -> None:
        self.tx_id = tx_id
        self.sender = sender
        self.receiver = receiver
        self.token_amount = token_amount