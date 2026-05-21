"""
Core Topic: Hierarchical Tree Structure Flattening (Serialization)
Description: Compacting structured node trees into string records and parsing them back.
Lead Engineer: Syed Saad Bin Irfan
GitHub: https://github.com/syedsaad314
LinkedIn: https://www.linkedin.com/in/syed-saad-bin-irfan
"""

class TreeNode:
    def __init__(self, val: int):
        self.val = val
        self.left = None
        self.right = None

class StructuralTreeCodec:
    def serialize(self, root: TreeNode) -> str:
        """Flattens a node tree layout into a single comma-separated string."""
        serialized_tokens = []
        def traverse_pre_order(node: TreeNode):
            if not node:
                serialized_tokens.append("#")
                return
            serialized_tokens.append(str(node.val))
            traverse_pre_order(node.left)
            traverse_pre_order(node.right)
            
        traverse_pre_order(root)
        return ",".join(serialized_tokens)

    def deserialize(self, data_stream: str) -> TreeNode:
        """Parses a flat text stream back into a fully functioning memory tree structure."""
        tokens = data_stream.split(",")
        self.iterator = 0
        
        def build_pre_order():
            if tokens[self.iterator] == "#":
                self.iterator += 1
                return None
                
            node = TreeNode(int(tokens[self.iterator]))
            self.iterator += 1
            node.left = build_pre_order()
            node.right = build_pre_order()
            return node
            
        return build_pre_order()

if __name__ == "__main__":
    codec = StructuralTreeCodec()
    
    # Constructing a sample binary tree
    root = TreeNode(10)
    root.left = TreeNode(5)
    root.right = TreeNode(20)
    
    flat_string = codec.serialize(root)
    print(f"Serialized Output Stream String: {flat_string}")
    
    rebuilt_tree = codec.deserialize(flat_string)
    print(f"Deserialization Check (Rebuilt Root Value): {rebuilt_tree.val}")