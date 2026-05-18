"""
CORE CONCEPT: Prefix Trie String Tokenizer Space
Building a nested prefix lookup tree node dictionary architecture from scratch.
Provides structured string insertion, retrieval tracking, and partial prefix scans 
for text processing applications.
"""

class TrieNode:
    def __init__(self):
        # Maps structural string characters to child node instance mappings
        self.children: dict[str, TrieNode] = {}
        # Boolean state property tracking terminal character string terminations
        self.is_terminal_word = False


class PrefixTokenizerTrie:
    def __init__(self):
        self.root = TrieNode()

    def insert_token(self, token_string: str) -> None:
        """Maps character strings into nested key structures, creating nodes dynamically."""
        current_layer = self.root
        for character in token_string:
            if character not in current_layer.children:
                current_layer.children[character] = TrieNode()
            current_layer = current_layer.children[character]
        current_layer.is_terminal_word = True

    def search_exact_token(self, token_string: str) -> bool:
        """Verifies if an exact character sequence matches a terminal token inside the trie."""
        current_layer = self.root
        for character in token_string:
            if character not in current_layer.children:
                return False
            current_layer = current_layer.children[character]
        return current_layer.is_terminal_word

    def starts_with_prefix(self, prefix_string: str) -> bool:
        """Validates if any stored token matches the provided starting sequence prefix."""
        current_layer = self.root
        for character in prefix_string:
            if character not in current_layer.children:
                return False
            current_layer = current_layer.children[character]
        return True


if __name__ == "__main__":
    trie = PrefixTokenizerTrie()
    trie.insert_token("tensor")
    trie.insert_token("transformer")

    print(f"Search Exact 'tensor': {trie.search_exact_token('tensor')}")
    print(f"Search Exact 'tens': {trie.search_exact_token('tens')}")
    print(f"Validate Prefix 'trans': {trie.starts_with_prefix('trans')}")