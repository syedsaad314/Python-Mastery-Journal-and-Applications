"""
Core Topic: Knuth-Morris-Pratt (KMP) String Matching
Description: Optimizes single-pattern lookups using a partial match table to prevent pointer backtracking.
Lead Engineer: Syed Saad Bin Irfan
GitHub: https://github.com/syedsaad314
LinkedIn: https://www.linkedin.com/in/syed-saad-bin-irfan
"""

from typing import List

class KMPMatcher:
    def __init__(self, pattern: str) -> None:
        self.pattern: str = pattern
        self.m: int = len(pattern)
        # Precompute the longest proper prefix which is also a suffix (LPS array)
        self.lps: List[int] = [0] * self.m
        if self.m > 0:
            self._compute_lps()

    def _compute_lps(self) -> None:
        """Fills the LPS failure array based on pattern self-similarity."""
        length = 0  # Length of the previous longest prefix suffix
        i = 1
        while i < self.m:
            if self.pattern[i] == self.pattern[length]:
                length += 1
                self.lps[i] = length
                i += 1
            else:
                if length != 0:
                    length = self.lps[length - 1]
                else:
                    self.lps[i] = 0
                    i += 1

    def search_in(self, text: str) -> List[int]:
        """Returns all 0-indexed starting positions where the pattern matches the text."""
        n = len(text)
        match_indices: List[int] = []
        if self.m == 0 or n < self.m:
            return match_indices

        i = 0  # Pointer for text
        j = 0  # Pointer for pattern
        while i < n:
            if text[i] == self.pattern[j]:
                i += 1
                j += 1

            if j == self.m:
                # Pattern found; calculate original starting index
                match_indices.append(i - j)
                j = self.lps[j - 1]
            elif i < n and text[i] != self.pattern[j]:
                # Mismatch detected; skip redundant comparisons using the LPS table
                if j != 0:
                    j = self.lps[j - 1]
                else:
                    i += 1

        return match_indices


if __name__ == "__main__":
    search_engine = KMPMatcher("ABABCABAB")
    sample_text = "ABABDABABCABABABABCABAB"
    
    results = search_engine.search_in(sample_text)
    print(f"Pattern found at indices: {results}")