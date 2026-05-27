"""
Core Topic: Text Indexing Structure (Suffix Array & LCP Array)
Description: Generates a sorted index of all string suffixes alongside a Longest Common Prefix matrix.
Lead Engineer: Syed Saad Bin Irfan
GitHub: https://github.com/syedsaad314
LinkedIn: https://www.linkedin.com/in/syed-saad-bin-irfan
"""

from typing import List

class SuffixArray:
    def __init__(self, text: str) -> None:
        self.text: str = text
        self.n: int = len(text)
        self.suffix_array: List[int] = []
        self.lcp_array: List[int] = [0] * self.n
        if self.n > 0:
            self._build_suffix_array()
            self._build_lcp_array()

    def _build_suffix_array(self) -> None:
        """Constructs the sorted index of suffixes using prefix doubling techniques."""
        # Initial ranking based on single-character ASCII values
        suffixes = [(self.text[i], i) for i in range(self.n)]
        suffixes.sort()
        
        ranks = [0] * self.n
        sa = [rank_item[1] for rank_item in suffixes]
        
        # Assign initial ranks
        r = 0
        ranks[sa[0]] = 0
        for i in range(1, self.n):
            if self.text[sa[i]] != self.text[sa[i - 1]]:
                r += 1
            ranks[sa[i]] = r

        # Prefix doubling: sort suffixes using pairs of ranks from previous iterations
        k = 1
        while k < self.n:
            # Create sort keys: (current_rank, rank_of_suffix_plus_k, original_index)
            sort_keys = []
            for i in range(self.n):
                next_rank = ranks[i + k] if i + k < self.n else -1
                sort_keys.append((ranks[i], next_rank, i))
                
            sort_keys.sort()
            sa = [item[2] for item in sort_keys]
            
            # Recalculate ranks based on the new sorted pairs
            new_ranks = [0] * self.n
            r = 0
            new_ranks[sa[0]] = 0
            for i in range(1, self.n):
                prev = sort_keys[i - 1]
                curr = sort_keys[i]
                if curr[0] != prev[0] or curr[1] != prev[1]:
                    r += 1
                new_ranks[sa[i]] = r
                
            ranks = new_ranks
            if r == self.n - 1:
                break
            k *= 2

        self.suffix_array = sa

    def _build_lcp_array(self) -> None:
        """Generates the Longest Common Prefix array in linear time using Kasai's algorithm."""
        rank_map = [0] * self.n
        for i, sa_val in enumerate(self.suffix_array):
            rank_map[sa_val] = i
            
        match_len = 0
        for i in range(self.n):
            if rank_map[i] == self.n - 1:
                match_len = 0
                continue
                
            # Find the next adjacent suffix in the sorted suffix array
            next_suffix_idx = self.suffix_array[rank_map[i] + 1]
            
            # Expand and count matching characters
            while (i + match_len < self.n and 
                   next_suffix_idx + match_len < self.n and 
                   self.text[i + match_len] == self.text[next_suffix_idx + match_len]):
                match_len += 1
                
            self.lcp_array[rank_map[i]] = match_len
            if match_len > 0:
                match_len -= 1


if __name__ == "__main__":
    indexer = SuffixArray("banana")
    
    print(f"Sorted Suffix Array Index: {indexer.suffix_array}") 
    # Order: [5, 3, 1, 0, 4, 2] -> corresponding to suffixes: a, ana, anana, banana, na, nana
    print(f"Longest Common Prefix Array: {indexer.lcp_array}")