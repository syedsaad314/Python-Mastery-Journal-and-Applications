"""
Core Topic: Replicated State Machine (RSM) Processing
Description: Commits and applies verified distributed log updates to an isolated database state machine.
Lead Engineer: Syed Saad Bin Irfan
"""

from typing import List, Dict, Tuple

class ReplicatedKeyValueStateMachine:
    """An isolated key-value store driven by log appends to maintain cluster consistency."""
    
    def __init__(self) -> None:
        self.underlying_store: Dict[str, str] = {}
        self.last_applied_index: int = 0

    def apply_log_entries(self, log_history: List[Tuple[int, str]], commit_index: int) -> int:
        """Appends and applies any committed entries to the state machine up to the commit index."""
        while self.last_applied_index < commit_index:
            self.last_applied_index += 1
            command_string = log_history[self.last_applied_index][1]
            self._execute_command(command_string)
            
        return self.last_applied_index

    def _execute_command(self, command: str) -> None:
        """Parses and runs state mutation string commands against the internal key-value store."""
        if command.startswith("PUT "):
            # Syntax structure format: "PUT key=value"
            parts = command[4:].split("=")
            if len(parts) == 2:
                self.underlying_store[parts[0].strip()] = parts[1].strip()
        elif command.startswith("DEL "):
            target_key = command[4:].strip()
            if target_key in self.underlying_store:
                del self.underlying_store[target_key]


if __name__ == "__main__":
    print("[RSM-CORE] Spinning up isolated state engine context...")
    rsm = ReplicatedKeyValueStateMachine()
    
    # Mock log history matching standard consensus formats
    shared_consensus_log = [
        (0, "NO_OP"),
        (1, "PUT user_id=saad_2026"),
        (1, "PUT cluster_zone=ubit_alpha"),
        (1, "DEL cluster_zone")
    ]

    # Advance the commit index to apply the first two mutations
    rsm.apply_log_entries(shared_consensus_log, commit_index=2)
    print(f"[RSM-CORE] State Map at Commit Index 2: {rsm.underlying_store}")

    # Advance the commit index to process the delete operation
    rsm.apply_log_entries(shared_consensus_log, commit_index=3)
    print(f"[RSM-CORE] Final State Map at Commit Index 3: {rsm.underlying_store}")