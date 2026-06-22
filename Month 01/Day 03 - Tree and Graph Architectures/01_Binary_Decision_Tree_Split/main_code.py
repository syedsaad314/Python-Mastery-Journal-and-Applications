"""
CORE CONCEPT: Binary Decision Tree Split Router
Constructing an object-oriented structural node framework capable of evaluating continuous 
feature vector inputs and routing data observations through conditional thresholds.
Forms the native runtime backbone of tree-based inferencing engines.
"""

from typing import Any, Optional

class DecisionNode:
    def __init__(
        self, 
        feature_index: Optional[int] = None, 
        threshold: Optional[float] = None, 
        left: Optional['DecisionNode'] = None, 
        right: Optional['DecisionNode'] = None, 
        value: Optional[Any] = None
    ):
        # Index of the feature column evaluated at this conditional split point
        self.feature_index = feature_index
        # Floating point cutoff limit determining left vs right structural split routing
        self.threshold = threshold
        # Left pointer branch (evaluated when observation feature vector value < threshold)
        self.left = left
        # Right pointer branch (evaluated when observation feature vector value >= threshold)
        self.right = right
        # Output terminal value; populated only if the node acts as an architectural leaf
        self.value = value

    @property
    def is_leaf(self) -> bool:
        """Determines if the current structural instance operates as a terminal node."""
        return self.value is not None

    def route_sample(self, sample_features: list[float]) -> Any:
        """Traverses down the tree hierarchy recursively to resolve classification/regression outputs."""
        if self.is_leaf:
            return self.value
            
        if self.feature_index is None or self.threshold is None:
            raise ValueError("Structural internal nodes must hold clear criteria dimensions.")

        if sample_features[self.feature_index] < self.threshold:
            if self.left is None:
                raise RuntimeError("Unbalanced tree routing state: Left pointer missing.")
            return self.left.route_sample(sample_features)
        else:
            if self.right is None:
                raise RuntimeError("Unbalanced tree routing state: Right pointer missing.")
            return self.right.route_sample(sample_features)


if __name__ == "__main__":
    # Simulate a miniature root decision engine: Is Age < 30 and Income >= 50000?
    leaf_young_low_income = DecisionNode(value="Target Group A")
    leaf_young_high_income = DecisionNode(value="Target Group B")
    leaf_senior = DecisionNode(value="Target Group C")

    # Lower conditional layer evaluating Income (Feature index 1) at a $50,000 threshold
    income_split = DecisionNode(feature_index=1, threshold=50000.0, left=leaf_young_low_income, right=leaf_young_high_income)
    # Master Root node evaluating Age (Feature index 0) at a 30.0 threshold
    root_node = DecisionNode(feature_index=0, threshold=30.0, left=income_split, right=leaf_senior)

    # Mock user entry profiles: [Age, Income]
    user_alpha = [24.5, 62000.0]
    user_beta  = [45.0, 15000.0]

    print(f"User Alpha Routing Target: {root_node.route_sample(user_alpha)}")
    print(f"User Beta Routing Target: {root_node.route_sample(user_beta)}")