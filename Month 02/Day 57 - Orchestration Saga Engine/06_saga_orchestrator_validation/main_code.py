# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Saga Orchestrator Transition Validation Gates
Description: Enforces strict state transition paths to keep the saga engine 
             from skipping critical recovery sequences.
"""
class SagaTransitionValidator:
    def __init__(self) -> None:
        self.state_flow_matrix = {
            "PENDING": ["RUNNING"],
            "RUNNING": ["SUCCESSFUL", "COMPENSATING"],
            "COMPENSATING": ["FAILED"],
            "SUCCESSFUL": [],
            "FAILED": []
        }

    def verify_state_step(self, historical_state: str, next_state: str) -> bool:
        allowed_paths = self.state_flow_matrix.get(historical_state, [])
        return next_state in allowed_paths

if __name__ == "__main__":
    validator = SagaTransitionValidator()
    
    # Valid tracking transitions
    assert validator.verify_state_step("RUNNING", "COMPENSATING") == True
    # Invalid tracking transitions (jumping directly to success from a failure recovery track)
    assert validator.verify_state_step("COMPENSATING", "SUCCESSFUL") == False