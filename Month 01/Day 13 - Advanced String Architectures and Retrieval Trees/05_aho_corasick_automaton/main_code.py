"""
Core Topic: Aho-Corasick Multi-Pattern Automation
Description: Combines a Trie with BFS failure links to match multiple patterns in a single pass.
Lead Engineer: Syed Saad Bin Irfan
GitHub: https://github.com/syedsaad314
LinkedIn: https://www.linkedin.com/in/syed-saad-bin-irfan
"""

from collections import deque
from typing import Dict, List

class AutomatonNode:
    def __init__(self) -> None:
        self.children: Dict[str, AutomatonNode] = {}
        self.fail_link: 'AutomatonNode' = None
        self.output_patterns: List[str] = []

class AhoCorasickAutomaton:
    def __init__(self) -> None:
        self.root: AutomatonNode = AutomatonNode()

    def insert_patterns(self, patterns: List[str]) -> None:
        """Populates the initial Trie structure with all target keywords."""
        for pattern in patterns:
            current = self.root
            for char in pattern:
                if char not in current.children:
                    current.children[char] = AutomatonNode()
                current = current.children[char]
            current.output_patterns.append(pattern)

    def construct_failure_links(self) -> None:
        """Builds BFS failure links across the tree structure to handle parsing errors."""
        queue: deque[AutomatonNode] = deque()
        
        # Initialize root level children pointing their failure links back to root
        for char, child in self.root.children.items():
            child.fail_link = self.root
            queue.append(child)

        while queue:
            current = queue.popleft()

            for char, child in current.children.items():
                fallback = current.fail_link
                while fallback is not None and char not in fallback.children:
                    fallback = fallback.fail_link
                
                child.fail_link = fallback.children[char] if fallback else self.root
                # Merge patterns to capture overlapping matches
                child.output_patterns.extend(child.fail_link.output_patterns)
                queue.append(child)

    def scan_text(self, text: str) -> Dict[str, List[int]]:
        """Parses text in a single, linear pass to find matches for all configured patterns."""
        results: Dict[str, List[int]] = {}
        current = self.root

        for idx, char in enumerate(text):
            while current is not None and char not in current.children:
                current = current.fail_link
            
            current = current.children[char] if current else self.root
            
            for pattern in current.output_patterns:
                if pattern not in results:
                    results[pattern] = []
                results[pattern].append(idx - len(pattern) + 1)
        return results


if __name__ == "__main__":
    automaton = AhoCorasickAutomaton()
    keywords = ["he", "she", "his", "hers"]
    
    automaton.insert_patterns(keywords)
    automaton.construct_failure_links()
    
    match_data = automaton.scan_text("ushersheishis")
    print("Multi-Pattern Scan Results:")
    for key, positions in match_data.items():
        print(f"Keyword '{key}' discovered at index positions: {positions}")