# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: State Machine Driver Execution
Description: Applies committed log commands sequentially to an isolated, 
             deterministic application state container.
"""
from typing import NamedTuple, Any, Dict

class LogEntry(NamedTuple):
    term: int
    index: int
    command: Dict[str, Any]

class LocalKeyValueStoreMachine:
    def __init__(self) -> None:
        self.kv_store: Dict[str, Any] = {}
        self.last_applied: int = 0

    def apply_committed_logs(self, log_history: list[LogEntry], commit_index: int) -> int:
        while self.last_applied < commit_index:
            entry_to_apply = log_history[self.last_applied]
            cmd = entry_to_apply.command
            
            if cmd.get("op") == "SET":
                self.kv_store[cmd["key"]] = cmd["val"]
                
            self.last_applied += 1
        return self.last_applied

if __name__ == "__main__":
    store = LocalKeyValueStoreMachine()
    logs = [LogEntry(1, 1, {"op": "SET", "key": "x", "val": 42})]
    
    applied_up_to = store.apply_committed_logs(logs, commit_index=1)
    assert applied_up_to == 1
    assert store.kv_store["x"] == 42