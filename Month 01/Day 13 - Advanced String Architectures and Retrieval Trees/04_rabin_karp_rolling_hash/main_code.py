"""
Core Topic: Rabin-Karp Rolling Hash Engine
Description: String matching via polynomial hash transformations and prime modulus arithmetic.
Lead Engineer: Syed Saad Bin Irfan
GitHub: https://github.com/syedsaad314
LinkedIn: https://www.linkedin.com/in/syed-saad-bin-irfan
"""

from typing import List

class RabinKarpMatcher:
    def __init__(self, alphabet_size: int = 256, prime_mod: int = 101) -> None:
        self.d: int = alphabet_size
        self.q: int = prime_mod

    def search(self, text: str, pattern: str) -> List[int]:
        """Calculates window hashes dynamically to isolate pattern matches in a text corpus."""
        n: int = len(text)
        m: int = len(pattern)
        if m == 0 or m > n: return []

        match_positions: List[int] = []
        pattern_hash: int = 0
        window_hash: int = 0
        h: int = 1

        # The value of h would be "pow(d, m-1) % q"
        for _ in range(m - 1):
            h = (h * self.d) % self.q

        # Step 1: Calculate initial baseline hash values for pattern and first window
        for i in range(m):
            pattern_hash = (self.d * pattern_hash + ord(pattern[i])) % self.q
            window_hash = (self.d * window_hash + ord(text[i])) % self.q

        # Step 2: Slide the window across the text body step-by-step
        for i in range(n - m + 1):
            if pattern_hash == window_hash:
                # Resolve hash collisions by doing an exact character check
                if text[i : i + m] == pattern:
                    match_positions.append(i)

            if i < n - m:
                # Compute the rolling hash value for the next window in O(1) time
                window_hash = (self.d * (window_hash - ord(text[i]) * h) + ord(text[i + m])) % self.q
                # Ensure the calculated hash value is non-negative
                if window_hash < 0:
                    window_hash += self.q

        return match_positions


if __name__ == "__main__":
    matcher = RabinKarpMatcher(alphabet_size=256, prime_mod=101)
    corpus = "GEEKS FOR GEEKS"
    target = "GEEK"
    
    locations = matcher.search(corpus, target)
    print(f"Rabin-Karp found pattern hits at: {locations}")