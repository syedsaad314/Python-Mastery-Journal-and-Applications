"""
Core Topic: Self-Balancing AVL Tree Implementation
Description: Using height-balanced balancing nodes and localized tree rotations to avoid worst-case linear lookup conditions.
Lead Engineer: Syed Saad Bin Irfan
GitHub: https://github.com/syedsaad314
LinkedIn: https://www.linkedin.com/in/syed-saad-bin-irfan
"""

class AVLNode:
    def __init__(self, key: int):
        self.key = key
        self.height = 1
        self.left = None
        self.right = None

class AVLTree:
    def get_height(self, node: AVLNode) -> int:
        return node.height if node else 0

    def get_balance_factor(self, node: AVLNode) -> int:
        return self.get_height(node.left) - self.get_height(node.right) if node else 0

    def rotate_right(self, y: AVLNode) -> AVLNode:
        """Performs a single right rotation to balance left-heavy subtrees."""
        x = y.left
        T2 = x.right
        
        x.right = y
        y.left = T2
        
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))
        return x

    def rotate_left(self, x: AVLNode) -> AVLNode:
        """Performs a single left rotation to balance right-heavy subtrees."""
        y = x.right
        T2 = y.left
        
        y.left = x
        x.right = T2
        
        x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        return y

    def insert(self, root: AVLNode, key: int) -> AVLNode:
        """Recursively places keys into correct slots, performing real-time structural rebalancing."""
        if not root:
            return AVLNode(key)
            
        if key < root.key:
            root.left = self.insert(root.left, key)
        elif key > root.key:
            root.right = self.insert(root.right, key)
        else:
            return root

        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))
        balance = self.get_balance_factor(root)

        # Case 1: Left-Left Heavy
        if balance > 1 and key < root.left.key:
            return self.rotate_right(root)
            
        # Case 2: Right-Right Heavy
        if balance < -1 and key > root.right.key:
            return self.rotate_left(root)
            
        # Case 3: Left-Right Heavy
        if balance > 1 and key > root.left.key:
            root.left = self.rotate_left(root.left)
            return self.rotate_right(root)
            
        # Case 4: Right-Left Heavy
        if balance < -1 and key < root.right.key:
            root.right = self.rotate_right(root.right)
            return self.rotate_left(root)

        return root

    def get_in_order_layout(self, root: AVLNode, result: list) -> None:
        if root:
            self.get_in_order_layout(root.left, result)
            result.append(root.key)
            self.get_in_order_layout(root.right, result)

if __name__ == "__main__":
    tree = AVLTree()
    root_node = None
    
    # Inserting sequentially increasing metrics to force structural self-rebalancing
    metrics = [10, 20, 30, 40, 50, 25]
    for element in metrics:
        root_node = tree.insert(root_node, element)
        
    ordered_list = []
    tree.get_in_order_layout(root_node, ordered_list)
    print(f"Balanced In-Order Vector Sequence: {ordered_list}")
    print(f"Optimized Root Node Configuration Location: {root_node.key}")