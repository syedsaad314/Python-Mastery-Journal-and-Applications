"""
Core Topic: Linear String Processing (Z-Algorithm)
Description: Constructs a Z-array tracking exact prefix matches across a unified string space.
Lead Engineer: Syed Saad Bin Irfan
GitHub: https://github.com/syedsaad314
LinkedIn: https://www.linkedin.com/in/syed-saad-bin-irfan
"""

from typing import List

class ZAlgorithm:
    @staticmethod
    def construct_z_array(unified_string: str) -> List[int]:
        """Builds a Z-array where each index tracks the longest common prefix with the start string."""
        n = len(unified_string)
        z = [0] * n
        if n == 0:
            return z

        # Establish boundary limits for the rightmost matching window [L, R]
        left, right = 0, 0

        for i in range(1, n):
            if i <= right:
                # Use previously calculated values inside the current window
                k = i - left
                if z[k] < right - i + 1:
                    z[i] = z[k]
                    continue
                # If the match extends beyond the window, shift the left boundary to re-evaluate
                left = i
            else:
                left = right = i

            # Manually expand the window to find additional matching characters
            while right < n and unified_string[right] == unified_string[right - left]:
                right += 1
            
            z[i] = right - left
            right -= 1  # Adjust boundary back to the last valid matching index

        return z

    def search_pattern(self, text: str, pattern: str) -> List[int]:
        """Locates all occurrences of a pattern inside a text stream in linear time."""
        if not text or not pattern or len(text) < len(pattern):
            return []

        # Combine pattern and text using a unique separator character
        combined = f"{pattern}${text}"
        z_array = self.construct_z_array(combined)
        
        pattern_length = len(pattern)
        match_indices = []

        # Find indices where the matching prefix length equals the pattern length
        for i in range(pattern_length + 1, len(combined)):
            if z_array[i] == pattern_length:
                # Map the index back to the original text positions
                match_indices.append(i - (pattern_length + 1))

        return match_indices


if __name__ == "__main__":
    engine = ZAlgorithm()
    target_text = "baabaabaah"
    target_pattern = "aaba"
    
    occurrences = engine.search_pattern(target_text, target_pattern)
    print(f"Pattern occurrences located at indices: {occurrences}")