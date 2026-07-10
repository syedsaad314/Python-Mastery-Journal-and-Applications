# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Dual-Phase Validation Gates
Description: Enforces strict structural transitions between the voting and 
             execution phases of a transaction.
"""
class TwoPhaseValidationGate:
    @staticmethod
    def validate_transition(current_phase: str, target_phase: str) -> bool:
        valid_paths = {
            "INIT": ["PREPARING"],
            "PREPARING": ["COMMITTED", "ABORTED"],
            "COMMITTED": [],
            "ABORTED": []
        }
        return target_phase in valid_paths.get(current_phase, [])

if __name__ == "__main__":
    # Valid transition path
    assert TwoPhaseValidationGate.validate_transition("INIT", "PREPARING") == True
    assert TwoPhaseValidationGate.validate_transition("PREPARING", "COMMITTED") == True
    # Invalid transition path (bypassing the voting phase)
    assert TwoPhaseValidationGate.validate_transition("INIT", "COMMITTED") == False