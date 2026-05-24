"""
Core Topic: Standard Trie Architecture (Prefix Tree)
Description: Efficient string storage and lookup engine using nested map references.
Lead Engineer: Syed Saad Bin Irfan
GitHub: https://github.com/syedsaad314
LinkedIn: https://www.linkedin.com/in/syed-saad-bin-irfan
"""

from typing import Dict

class TrieNode:
    def __init__(self) -> None:
        self.children: Dict[str, TrieNode] = {}
        self.is_end_of_word: bool = False

class TriePrefixTree:
    def __init__(self) -> None:
        self.root: TrieNode = TrieNode()

    def insert(self, word: str) -> None:
        """Inserts a word step-by-step into the retrieval tree structure."""
        current = self.root
        for char in word:
            if char not in current.children:
                current.children[char] = TrieNode()
            current = current.children[char]
        current.is_end_of_word = True

    def search(self, word: str) -> bool:
        """Checks for the exact existence of a complete string term."""
        current = self.root
        for char in word:
            if char not in current.children:
                return False
            current = current.children[char]
        return current.is_end_of_word

    def starts_with(self, prefix: str) -> bool:
        """Validates if any stored string contains the given search prefix."""
        current = self.root
        for char in prefix:
            if char not in current.children:
                return False
            current = current.children[char]
        return True


if __name__ == "__main__":
    trie = TriePrefixTree()
    trie.insert("software")
    trie.insert("systems")
    trie.insert("architecture")

    print(f"Search 'systems': {trie.search('systems')}")        # True
    print(f"Search 'architect': {trie.search('architect')}")    # False
    print(f"Prefix 'arch': {trie.starts_with('arch')}")          # True