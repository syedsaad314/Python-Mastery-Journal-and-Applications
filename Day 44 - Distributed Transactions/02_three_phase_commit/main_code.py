"""
Core Topic: Three-Phase Commit Protocol (3PC)
Description: Introduces non-blocking PreCommit intervals to mitigate coordinator crashes.
Lead Engineer: Syed Saad Bin Irfan
"""

from typing import List

class NonBlockingParticipant:
    def prepare(self) -> bool: return True
    def pre_commit(self) -> None: print("[PARTICIPANT] State prepared, entering non-blocking commit lock.")


class ThreePhaseCommitCoordinator:
    def __init__(self, participants: List[NonBlockingParticipant]) -> None:
        self.participants = participants

    def run_three_phase_cycle(self) -> bool:
        # 1. Can-Commit Phase
        votes = [p.prepare() for p in self.participants]
        if not all(votes): return False

        # 2. Pre-Commit Phase (Eliminates blocking vulnerabilities found in 2PC)
        for p in self.participants:
            p.pre_commit()

        # 3. Do-Commit Phase
        print("[3PC-COORDINATOR] Final execution commits dispatched smoothly.")
        return True


if __name__ == "__main__":
    cohort = [NonBlockingParticipant(), NonBlockingParticipant()]
    coordinator = ThreePhaseCommitCoordinator(cohort)
    assert coordinator.run_three_phase_cycle() == True