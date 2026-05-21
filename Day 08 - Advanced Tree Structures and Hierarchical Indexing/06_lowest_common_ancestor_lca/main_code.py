"""
Core Topic: Lowest Common Ancestor (LCA) Detection
Description: Resolving shared parent junctions within structured directory layouts.
Lead Engineer: Syed Saad Bin Irfan
GitHub: https://github.com/syedsaad314
LinkedIn: https://www.linkedin.com/in/syed-saad-bin-irfan
"""

class FolderNode:
    def __init__(self, name: str):
        self.name = name
        self.left = None
        self.right = None

class DependencyResolver:
    def find_lowest_common_ancestor(self, root: FolderNode, node_p: FolderNode, node_q: FolderNode) -> FolderNode:
        """Finds the lowest shared parent junction node between two target nodes."""
        if not root or root == node_p or root == node_q:
            return root
            
        left_branch = self.find_lowest_common_ancestor(root.left, node_p, node_q)
        right_branch = self.find_lowest_common_ancestor(root.right, node_p, node_q)
        
        # If both branches return values, the current node is the lowest common parent
        if left_branch and right_branch:
            return root
            
        return left_branch if left_branch else right_branch

if __name__ == "__main__":
    # Modeling a directory tree layout
    root_dir = FolderNode("root")
    root_dir.left = FolderNode("etc")
    root_dir.right = FolderNode("var")
    root_dir.left.left = FolderNode("nginx")
    root_dir.left.right = FolderNode("systemd")
    
    resolver = DependencyResolver()
    target_a = root_dir.left.left   # nginx
    target_b = root_dir.left.right  # systemd
    
    ancestor = resolver.find_lowest_common_ancestor(root_dir, target_a, target_b)
    print(f"Closest Shared Inheritance Parent Node: {ancestor.name}")