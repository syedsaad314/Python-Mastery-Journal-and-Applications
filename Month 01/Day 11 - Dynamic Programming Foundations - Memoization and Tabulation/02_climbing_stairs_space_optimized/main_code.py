"""
Core Topic: Constant-Space Linear Recurrences
Description: Optimizing structural state tracking arrays down to simple sliding memory variables.
Lead Engineer: Syed Saad Bin Irfan
GitHub: https://github.com/syedsaad314
LinkedIn: https://www.linkedin.com/in/syed-saad-bin-irfan
"""

class RecurrenceOptimizer:
    @staticmethod
    def compute_combinations(total_steps: int) -> int:
        """Calculates combination sets cleanly using state-shifting variables instead of an array."""
        if total_steps <= 2:
            return total_steps
            
        # Initialize variables representing the last two step tracking points
        two_steps_back = 1
        one_step_back = 2
        
        for _ in range(3, total_steps + 1):
            current_accumulation = one_step_back + two_steps_back
            # Shift state registers forward
            two_steps_back = one_step_back
            one_step_back = current_accumulation
            
        return one_step_back

if __name__ == "__main__":
    target_steps = 10
    total_paths = RecurrenceOptimizer.compute_combinations(target_steps)
    print(f"Total Unique Valid Combinations across [{target_steps}] Steps: {total_paths}")