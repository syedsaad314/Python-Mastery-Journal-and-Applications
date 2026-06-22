"""
Core Topic: Longest Common Subsequence (LCS)
Description: 2D string matching engine detecting shared structural patterns across divergent text.
Lead Engineer: Syed Saad Bin Irfan
GitHub: https://github.com/syedsaad314
LinkedIn: https://www.linkedin.com/in/syed-saad-bin-irfan
"""

class SequenceAligner:
    @staticmethod
    def compute_lcs(text1: str, text2: str) -> int:
        """Compares two strings to calculate the deepest shared sequence of characters."""
        len1, len2 = len(text1), len(text2)
        # 2D tracking matrix with a buffer row/col of zeros for baseline conditions
        dp_matrix = [[0] * (len2 + 1) for _ in range(len1 + 1)]
        
        for row in range(1, len1 + 1):
            for col in range(1, len2 + 1):
                if text1[row - 1] == text2[col - 1]:
                    # Match found: extend the diagonal history by 1
                    dp_matrix[row][col] = dp_matrix[row - 1][col - 1] + 1
                else:
                    # Mismatch: carry forward the highest value from adjacent states
                    dp_matrix[row][col] = max(dp_matrix[row - 1][col], dp_matrix[row][col - 1])
                    
        return dp_matrix[len1][len2]

if __name__ == "__main__":
    primary_stream = "abcde"
    secondary_stream = "ace"
    
    alignment_score = SequenceAligner.compute_lcs(primary_stream, secondary_stream)
    print(f"Deepest Shared Sequence Length between '{primary_stream}' and '{secondary_stream}': {alignment_score}")