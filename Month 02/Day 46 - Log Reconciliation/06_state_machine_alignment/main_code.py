# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: State Machine Alignment
Description: Validates that local state machine updates only run up to the leader's commit index boundary.
"""

from typing import List, Dict

class StateMachineAligner:
    @staticmethod
    def apply_committed_logs(log: List[Dict[str, any]], current_state: dict, commit_index: int) -> dict:
        for idx in range(0, commit_index + 1):
            if idx < len(log):
                cmd = log[idx]["command"]
                key, val = cmd.replace("SET ", "").split("=")
                current_state[key.strip()] = val.strip()
        return current_state

if __name__ == "__main__":
    runtime_log = [{"command": "SET a=1"}, {"command": "SET b=2"}]
    state_store = {}
    updated_store = StateMachineAligner.apply_committed_logs(runtime_log, state_store, commit_index=0)
    assert "a" in updated_store
    assert "b" not in updated_store