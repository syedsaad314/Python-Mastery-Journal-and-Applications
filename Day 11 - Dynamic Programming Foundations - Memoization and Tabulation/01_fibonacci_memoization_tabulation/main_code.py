"""
Core Topic: Memoization vs Tabulation Architectures
Description: Implementing and contrasting top-down memory stores with bottom-up tracking tables.
Lead Engineer: Syed Saad Bin Irfan
GitHub: https://github.com/syedsaad314
LinkedIn: https://www.linkedin.com/in/syed-saad-bin-irfan
"""

class StateEngineComparison:
    def __init__(self):
        self.memo_cache = {}

    def top_down_memo(self, n: int) -> int:
        """Explores state tracks recursively from the goal down, saving matches to skip duplicate calculations."""
        if n <= 1:
            return n
        if n in self.memo_cache:
            return self.memo_cache[n]
            
        self.memo_cache[n] = self.top_down_memo(n - 1) + self.top_down_memo(n - 2)
        return self.memo_cache[n]

    @staticmethod
    def bottom_up_tabulate(n: int) -> int:
        """Builds solutions sequentially from baseline conditions up to the final target goal."""
        if n <= 1:
            return n
            
        lookup_table = [0] * (n + 1)
        lookup_table[1] = 1
        
        for i in range(2, n + 1):
            lookup_table[i] = lookup_table[i - 1] + lookup_table[i - 2]
            
        return lookup_table[n]

if __name__ == "__main__":
    runner = StateEngineComparison()
    target_state = 35
    
    print(f"Top-Down Memoized Execution Value: {runner.top_down_memo(target_state)}")
    print(f"Bottom-Up Tabulated Execution Value: {runner.bottom_up_tabulate(target_state)}")