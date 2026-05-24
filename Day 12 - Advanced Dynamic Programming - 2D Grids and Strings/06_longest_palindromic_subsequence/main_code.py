"""
Core Topic: Longest Palindromic Subsequence (LPS) via 2D Tabulation
Description: Minimizing state overlaps to find the longest symmetric character sequence within a single string.
Lead Engineer: Syed Saad Bin Irfan
GitHub: https://github.com/syedsaad314
LinkedIn: https://www.linkedin.com/in/syed-saad-bin-irfan
"""

class PalindromeSequenceAnalyzer:
    @staticmethod
    def compute_longest_palindrome_subseq(sequence: str) -> int:
        """Calculates the maximum length of a palindromic subsequence using a 2D state matrix."""
        if not sequence:
            return 0
            
        seq_len = len(sequence)
        # Allocate a 2D matrix where dp[i][j] tracks the LPS length from index i to j
        dp_table = [[0] * seq_len for _ in range(seq_len)]
        
        # Base Case: Single characters are inherently palindromes of length 1
        for i in range(seq_len):
            dp_table[i][i] = 1
            
        # Shift the evaluation window across the string length
        for window_size in range(2, seq_len + 1):
            for start_idx in range(seq_len - window_size + 1):
                end_idx = start_idx + window_size - 1
                
                # Condition 1: Outer boundaries match perfectly
                if sequence[start_idx] == sequence[end_idx]:
                    if window_size == 2:
                        dp_table[start_idx][end_idx] = 2
                    else:
                        dp_table[start_idx][end_idx] = dp_table[start_idx + 1][end_idx - 1] + 2
                # Condition 2: Boundaries conflict, maximize by discarding one edge character
                else:
                    dp_table[start_idx][end_idx] = max(
                        dp_table[start_idx + 1][end_idx],
                        dp_table[start_idx][end_idx - 1]
                    )
                    
        return dp_table[0][seq_len - 1]

if __name__ == "__main__":
    target_string = "bbbab"
    max_lps_length = PalindromeSequenceAnalyzer.compute_longest_palindrome_subseq(target_string)
    print(f"Longest Palindromic Subsequence Length inside '{target_string}': {max_lps_length}")