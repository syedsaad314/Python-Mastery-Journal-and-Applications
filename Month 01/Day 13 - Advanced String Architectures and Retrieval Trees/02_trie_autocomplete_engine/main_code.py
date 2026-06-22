"""
Core Topic: Auto-Complete Engine Extensions
Description: Trie architecture with recursive DFS scanning to query prefix options.
Lead Engineer: Syed Saad Bin Irfan
GitHub: https://github.com/syedsaad314
LinkedIn: https://www.linkedin.com/in/syed-saad-bin-irfan
"""

from typing import Dict, List

class AutoCompleteNode:
    def __init__(self) -> __init__:
        self.children: Dict[str, AutoCompleteNode] = {}
        self.is_end_of_word: bool = False

class TrieAutoCompleteEngine:
    def __init__(self) -> None:
        self.root: AutoCompleteNode = AutoCompleteNode()

    def insert(self, word: str) -> None:
        """Populates the auto-complete lookup tree structure."""
        current = self.root
        for char in word:
            if char not in current.children:
                current.children[char] = AutoCompleteNode()
            current = current.children[char]
        current.is_end_of_word = True

    def _collect_words_dfs(self, node: AutoCompleteNode, prefix: str, outcomes: List[str]) -> None:
        """Traverses downward from a prefix node to gather all potential word variants."""
        if node.is_end_of_word:
            outcomes.append(prefix)
        
        for char, child_node in node.children.items():
            self._collect_words_dfs(child_node, prefix + char, outcomes)

    def query_predictions(self, prefix: str) -> List[str]:
        """Locates the terminal prefix node, then runs a DFS to find suggestion strings."""
        current = self.root
        for char in prefix:
            if char not in current.children:
                return []
            current = current.children[char]
        
        suggestions: List[str] = []
        self._collect_words_dfs(current, prefix, suggestions)
        return suggestions


if __name__ == "__main__":
    engine = TrieAutoCompleteEngine()
    engine.insert("kafka")
    engine.insert("kahn")
    engine.insert("karachi")
    engine.insert("kotlin")

    print(f"Suggestions for 'ka': {engine.query_predictions('ka')}")
    print(f"Suggestions for 'kot': {engine.query_predictions('kot')}")