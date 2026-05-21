"""
Core Topic: Prefix Trie Directory Mapping Engine
Description: Using nested child character records to execute fast string lookups.
Lead Engineer: Syed Saad Bin Irfan
GitHub: https://github.com/syedsaad314
LinkedIn: https://www.linkedin.com/in/syed-saad-bin-irfan
"""

class TrieNode:
    def __init__(self):
        # Character mapping map pointers to downstream TrieNodes
        self.children = {}
        self.is_terminal_point = False

class RoutingPrefixTrie:
    def __init__(self):
        self.root = TrieNode()

    def register_route(self, path_string: str) -> None:
        """Splits incoming character elements out to establish nested character paths."""
        current_node = self.root
        for character in path_string:
            if character not in current_node.children:
                current_node.children[character] = TrieNode()
            current_node = current_node.children[character]
        current_node.is_terminal_point = True

    def match_prefix(self, prefix_string: str) -> bool:
        """Verifies if the prefix exists inside the directory lookup structure."""
        current_node = self.root
        for character in prefix_string:
            if character not in current_node.children:
                return False
            current_node = current_node.children[character]
        return True

if __name__ == "__main__":
    router = RoutingPrefixTrie()
    router.register_route("/api/v1/auth")
    router.register_route("/api/v1/users/profile")
    
    print(f"Prefix Match Check ('/api/v1'): {router.match_prefix('/api/v1')}")
    print(f"Prefix Match Check ('/api/v2'): {router.match_prefix('/api/v2')}")