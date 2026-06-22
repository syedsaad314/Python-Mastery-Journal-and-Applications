"""
CORE CONCEPT: Rolling Polynomial Hash Sequence Engine
Implementing a sliding window signature tracker using polynomial arithmetic. 
Computes sub-string hashes incrementally in constant time, forming the basis for 
sequence analysis without re-indexing the window.
"""

class RollingHashPipeline:
    def __init__(self, base: int = 256, prime_modulus: int = 101):
        self.base = base
        self.modulus = prime_modulus
        self.current_hash = 0
        self.window_size = 0
        self.highest_base_power = 1  # Equivalent to (base^(window_size - 1)) % modulus

    def compute_initial_hash(self, sequence: str, window_len: int) -> int:
        """Initializes the polynomial hash value across the starting sequence window."""
        self.window_size = window_len
        self.current_hash = 0
        self.highest_base_power = 1
        
        # Precompute the highest positional base multiplier factor
        for _ in range(window_len - 1):
            self.highest_base_power = (self.highest_base_power * self.base) % self.modulus
            
        for i in range(window_len):
            self.current_hash = (self.base * self.current_hash + ord(sequence[i])) % self.modulus
            
        return self.current_hash

    def slide_window(self, old_char: str, new_char: str) -> int:
        """Updates the hash value in constant time by sliding the window forward one step.

        old_char and new_char are expected to be single-character strings.
        """
        # Subtract the leading character's component
        self.current_hash = (self.current_hash - ord(old_char) * self.highest_base_power) % self.modulus
        
        # Add the trailing character's component
        self.current_hash = (self.current_hash * self.base + ord(new_char)) % self.modulus
        
        return self.current_hash


if __name__ == "__main__":
    stream_text = "AGCTTTTCATTCTGA"
    pipeline = RollingHashPipeline()
    
    initial = pipeline.compute_initial_hash(stream_text, window_len=4)
    print(f"Initial Window Hash ('AGCT'): {initial}")
    
    next_hash = pipeline.slide_window('A', 'T')
    print(f"Slid Window Hash ('GCTT'): {next_hash}")