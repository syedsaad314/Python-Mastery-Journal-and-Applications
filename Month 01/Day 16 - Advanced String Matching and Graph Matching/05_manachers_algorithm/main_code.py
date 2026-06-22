"""
Core Topic: Linear Palindromic Extraction (Manacher's Algorithm)
Description: Identifies the longest palindromic substring in pure linear time using mirrored center expansions.
Lead Engineer: Syed Saad Bin Irfan
GitHub: https://github.com/syedsaad314
LinkedIn: https://www.linkedin.com/in/syed-saad-bin-irfan
"""

from typing import List

class ManachersAlgorithm:
    def __init__(self, text: str) -> None:
        self.raw_text: str = text
        self.transformed: str = ""
        self.radii: List[int] = []
        self._normalize_string()

    def _normalize_string(self) -> None:
        """Inserts separator bounds to handle even and odd palindrome lengths uniformly."""
        if not self.raw_text:
            self.transformed = "^$"
            return
            
        # Wrap characters with special symbols to avoid boundary checks
        chars = ["^"]
        for c in self.raw_text:
            chars.extend(["#", c])
        chars.extend(["#", "$"])
        self.transformed = "".join(chars)
        self.radii = [0] * len(self.transformed)

    def extract_longest_palindrome(self) -> str:
        """Finds and returns the absolute longest palindromic substring in linear time."""
        if not self.raw_text:
            return ""

        n = len(self.transformed)
        center = 0
        right_boundary = 0

        for i in range(1, n - 1):
            # Calculate the mirror index across the current center point
            mirror = 2 * center - i

            if i < right_boundary:
                # Initialize the radius using the mirror property to skip redundant expansions
                self.radii[i] = min(right_boundary - i, self.radii[mirror])

            # Expand the palindrome symmetrically around index i
            while self.transformed[i + 1 + self.radii[i]] == self.transformed[i - 1 - self.radii[i]]:
                self.radii[i] += 1

            # If the palindrome extends past the current boundary, update the center and right edge
            if i + self.radii[i] > right_boundary:
                center = i
                right_boundary = i + self.radii[i]

        # Locate the index with the maximum calculated radius
        max_len = 0
        center_index = 0
        for idx, radius in enumerate(self.radii):
            if radius > max_len:
                max_len = radius
                center_index = idx

        # Extract the original substring by mapping back from the transformed string
        start = (center_index - max_len) // 2
        return self.raw_text[start : start + max_len]


if __name__ == "__main__":
    engine = ManachersAlgorithm("babad")
    longest_substring = engine.extract_longest_palindrome()
    print(f"Longest identified palindromic sequence: '{longest_substring}'")