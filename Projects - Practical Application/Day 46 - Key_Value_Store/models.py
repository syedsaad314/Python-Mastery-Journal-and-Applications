# Lead Engineer: Syed Saad Bin Irfan
"""
Component: Log Entry Data Structures
Description: Defines individual log entries that carry term numbers and state change commands.
"""

class LogEntry:
    def __init__(self, term: int, command: str) -> None:
        self.term = term
        self.command = command

    def to_dict(self) -> dict:
        return {"term": self.term, "command": self.command}