"""
Core Topic: Knuth-Morris-Pratt (KMP) Deterministic Automation
Description: Linearly matches patterns without index backtracking using an LPS table.
Lead Engineer: Syed Saad Bin Irfan
GitHub: https://github.com/syedsaad314
LinkedIn: https://www.linkedin.com/in/syed-saad-bin-irfan
"""

from typing import List

class KMPPatternMatcher:
    @staticmethod
    def compute_lps_table(pattern: str) -> List[int]:
        """Generates the Longest Prefix Suffix (LPS) array to skip redundant alignment checks."""
        m: int = len(pattern)
        lps: List[int] = [0] * m
        length: int = 0  # Length of the previous longest prefix suffix
        i: int = 1

        while i < m:
            if pattern[i] == pattern[length]:
                length += 1
                lps[i] = length
                i += 1
            else:
                if length != 0:
                    length = lps[length - 1]
                else:
                    lps[i] = 0
                    i += 1
        return lps

    @classmethod
    def execute_search(cls, text: str, pattern: str) -> List[int]:
        """Runs a linear-time scan across a text field to match the target pattern string."""
        n: int = len(text)
        m: int = len(pattern)
        if m == 0: return []

        lps: List[int] = cls.compute_lps_table(pattern)
        match_indices: List[int] = []
        i: int = 0  # Index tracker for text
        j: int = 0  # Index tracker for pattern

        while i < n:
            if pattern[j] == text[i]:
                i += 1
                j += 1

            if j == m:
                match_indices.append(i - j)
                j = lps[j - 1]
            elif i < n and pattern[j] != text[i]:
                if j != 0:
                    j = lps[j - 1]
                else:
                    i += 1
        return match_indices


if __name__ == "__main__":
    text_corpus = "ABABDABACDABABCABAB"
    search_pattern = "ABABCABAB"
    
    indices = KMPPatternMatcher.execute_search(text_corpus, search_pattern)
    print(f"Pattern detected at index positions: {indices}")