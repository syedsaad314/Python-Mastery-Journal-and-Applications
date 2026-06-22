"""
Core Topic: Edit Distance (Levenshtein Distance)
Description: Calculating the minimal operations required to mutate one string into another.
Lead Engineer: Syed Saad Bin Irfan
GitHub: https://github.com/syedsaad314
LinkedIn: https://www.linkedin.com/in/syed-saad-bin-irfan
"""

class StringMutator:
    @staticmethod
    def calculate_min_operations(source: str, target: str) -> int:
        """Determines the absolute minimum inserts, deletes, or replaces to match strings."""
        len_s, len_t = len(source), len(target)
        dp_matrix = [[0] * (len_t + 1) for _ in range(len_s + 1)]
        
        # Initialize base cases: converting empty strings requires N operations
        for i in range(len_s + 1):
            dp_matrix[i][0] = i
        for j in range(len_t + 1):
            dp_matrix[0][j] = j
            
        for i in range(1, len_s + 1):
            for j in range(1, len_t + 1):
                if source[i - 1] == target[j - 1]:
                    # Characters match: No operation needed, inherit diagonal state
                    dp_matrix[i][j] = dp_matrix[i - 1][j - 1]
                else:
                    # Mismatch transition: Find the cheapest operation and add 1
                    insert_op = dp_matrix[i][j - 1]
                    delete_op = dp_matrix[i - 1][j]
                    replace_op = dp_matrix[i - 1][j - 1]
                    
                    dp_matrix[i][j] = 1 + min(insert_op, delete_op, replace_op)
                    
        return dp_matrix[len_s][len_t]

if __name__ == "__main__":
    word_alpha = "intention"
    word_beta = "execution"
    
    mutation_cost = StringMutator.calculate_min_operations(word_alpha, word_beta)
    print(f"Minimum Operations to morph '{word_alpha}' into '{word_beta}': {mutation_cost}")