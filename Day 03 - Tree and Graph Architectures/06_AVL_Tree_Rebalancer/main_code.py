"""
CORE CONCEPT: Self-Balancing AVL Binary Search Tree Node
Constructing a balanced binary search tree node structure from scratch. Natively 
calculates subtree height imbalances and triggers pointer rotations to guarantee 
sub-linear search performance under heavy writes.
"""

from typing import Optional

class AVLNode:
    def __init__(self, key: float):
        self.key = key
        self.height: int = 1
        self.left: 'Optional[AVLNode]' = None
        self.right: 'Optional[AVLNode]' = None


class AVLTreeEngine:
    def get_height(self, node: Optional[AVLNode]) -> int:
        return node.height if node else 0

    def get_balance_factor(self, node: Optional[AVLNode]) -> int:
        if not node:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)

    def rotate_right(self, y: AVLNode) -> AVLNode:
        """Performs right pointer pivot transformation to lower left-heavy branch imbalances."""
        x = y.left
        T2 = x.right

        # Execute pointer remapping pivot step
        x.right = y
        y.left = T2

        # Adjust height records based on structural modifications
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))
        return x

    def rotate_left(self, x: AVLNode) -> AVLNode:
        """Performs left pointer pivot transformation to lower right-heavy branch imbalances."""
        y = x.right
        T2 = y.left

        # Execute pointer remapping pivot step
        y.left = x
        x.right = T2

        # Adjust height records based on structural modifications
        x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        return y

    def insert(self, root: Optional[AVLNode], key: float) -> AVLNode:
        """Inserts a numerical value recursively, applying necessary balance corrections."""
        if not root:
            return AVLNode(key)

        if key < root.key:
            root.left = self.insert(root.left, key)
        else:
            root.right = self.insert(root.right, key)

        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))
        balance = self.get_balance_factor(root)

        # Left-Heavy Imbalance Case
        if balance > 1 and key < root.left.key:
            return self.rotate_right(root)

        # Right-Heavy Imbalance Case
        if balance < -1 and key > root.right.key:
            return self.rotate_left(root)

        # Left-Right Double Imbalance Case
        if balance > 1 and key > root.left.key:
            root.left = self.rotate_left(root.left)
            return self.rotate_right(root)

        # Right-Left Double Imbalance Case
        if balance < -1 and key < root.right.key:
            root.right = self.rotate_right(root.right)
            return self.rotate_left(root)

        return root


if __name__ == "__main__":
    tree = AVLTreeEngine()
    root_node = None
    
    # Inserting sequentially ordered values that would break a standard un-balanced BST
    data_points = [10.0, 20.0, 30.0, 40.0, 50.0]
    for target_score in data_points:
        root_node = tree.insert(root_node, target_score)
        
    print(f"Balanced Master Root Node Coordinate Value: {root_node.key}")
    print(f"Overall Re-balanced Tree Depth Height: {root_node.height}")