"""
Core Topic: Multi-Pattern Automaton Dictionary Matching (Aho-Corasick)
Description: Evaluates multiple dictionary keywords simultaneously across a single text stream.
Lead Engineer: Syed Saad Bin Irfan
GitHub: https://github.com/syedsaad314
LinkedIn: https://www.linkedin.com/in/syed-saad-bin-irfan
"""

from collections import deque
from typing import Dict, List

class AhoCorasickNode:
    def __init__(self) -> None:
        self.children: Dict[str, 'AhoCorasickNode'] = {}
        self.fail_link: 'AhoCorasickNode' = None
        self.output_patterns: List[str] = []

class AhoCorasick:
    def __init__(self, patterns: List[str]) -> None:
        self.root = AhoCorasickNode()
        self.patterns = patterns
        self._build_trie()
        self._build_automaton_links()

    def _build_trie(self) -> None:
        """Inserts all target dictionary patterns into the underlying Trie structure."""
        for pattern in self.patterns:
            current = self.root
            for char in pattern:
                if char not in current.children:
                    current.children[char] = AhoCorasickNode()
                current = current.children[char]
            current.output_patterns.append(pattern)

    def _build_automaton_links(self) -> None:
        """Connects fallback links across trie nodes using Breadth-First Search (BFS)."""
        queue: deque['AhoCorasickNode'] = deque()
        
        # Initialize the first layer of nodes below the root
        for char, child in self.root.children.items():
            child.fail_link = self.root
            queue.append(child)
            
        while queue:
            current = queue.popleft()
            
            for char, child in current.children.items():
                # Trace back through failure paths to find the longest valid suffix match
                fallback = current.fail_link
                while fallback is not None and char not in fallback.children:
                    fallback = fallback.fail_link
                    
                child.fail_link = fallback.children[char] if fallback else self.root
                # Append found patterns from the fallback path to the current node's output
                child.output_patterns.extend(child.fail_link.output_patterns)
                queue.append(child)

    def search_in_text(self, text: str) -> Dict[str, List[int]]:
        """Scans text in a single pass, returning all matches found for every keyword."""
        match_map: Dict[str, List[int]] = {p: [] for p in self.patterns}
        current = self.root
        
        for idx, char in enumerate(text):
            # Fallback through failure links if the current character doesn't match any child node
            while current is not None and char not in current.children:
                current = current.fail_link
                
            if current is None:
                current = self.root
                continue
                
            current = current.children[char]
            # Log all pattern matches identified at this position
            for pattern in current.output_patterns:
                start_pos = idx - len(pattern) + 1
                match_map[pattern].append(start_pos)
                
        return match_map


if __name__ == "__main__":
    dictionary = ["he", "she", "his", "hers"]
    automaton = AhoCorasick(dictionary)
    
    stream_text = "ushersbehis"
    all_matches = automaton.search_in_text(stream_text)
    
    for word, positions in all_matches.items():
        print(f"Keyword '{word}' discovered at starting positions: {positions}")