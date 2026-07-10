# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Transaction Coordinator State Models
Description: Implements state machine containers and type tokens 
             representing coordinator lifecycle records.
"""
from enum import Enum
from typing import NamedTuple, List

class CoordinatorState(Enum):
    INIT = "INIT"
    PREPARING = "PREPARING"
    COMMITTED = "COMMITTED"
    ABORTED = "ABORTED"

class TransactionContext(NamedTuple):
    tx_id: str
    state: CoordinatorState
    participants: List[str]

if __name__ == "__main__":
    ctx = TransactionContext(
        tx_id="tx_9082",
        state=CoordinatorState.INIT,
        participants=["db_shard_01", "db_shard_02"]
    )
    assert ctx.tx_id == "tx_9082"
    assert ctx.state == CoordinatorState.INIT