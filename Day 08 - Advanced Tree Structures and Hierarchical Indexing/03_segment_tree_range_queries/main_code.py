"""
Core Topic: Segment Tree Interval Accumulator
Description: Partitioning arrays into balanced interval arrays to manage dynamic range queries.
Lead Engineer: Syed Saad Bin Irfan
GitHub: https://github.com/syedsaad314
LinkedIn: https://www.linkedin.com/in/syed-saad-bin-irfan
"""

class SegmentTree:
    def __init__(self, data_source: list[int]):
        self.n = len(data_source)
        # Size bounding allocation required for complete tracking trees
        self.tree = [0] * (4 * self.n)
        if self.n > 0:
            self._build_tree(data_source, 0, 0, self.n - 1)

    def _build_tree(self, data: list, tree_idx: int, left_bound: int, right_bound: int) -> None:
        if left_bound == right_bound:
            self.tree[tree_idx] = data[left_bound]
            return
            
        mid = (left_bound + right_bound) // 2
        self._build_tree(data, 2 * tree_idx + 1, left_bound, mid)
        self._build_tree(data, 2 * tree_idx + 2, mid + 1, right_bound)
        self.tree[tree_idx] = self.tree[2 * tree_idx + 1] + self.tree[2 * tree_idx + 2]

    def query_range(self, tree_idx: int, left: int, right: int, q_left: int, q_right: int) -> int:
        """Extracts sum totals for targeted range intervals without linear element scans."""
        if q_left <= left and right <= q_right:
            return self.tree[tree_idx]
        if right < q_left or left > q_right:
            return 0
            
        mid = (left + right) // 2
        return (self.query_range(2 * tree_idx + 1, left, mid, q_left, q_right) +
                self.query_range(2 * tree_idx + 2, mid + 1, right, q_left, q_right))

if __name__ == "__main__":
    telemetry_logs = [5, 12, 7, 3, 9, 1]
    engine = SegmentTree(telemetry_logs)
    
    # Query sum of elements from index 1 to 4 (12 + 7 + 3 + 9)
    total_range_sum = engine.query_range(0, 0, engine.n - 1, 1, 4)
    print(f"Calculated Aggregate Interval Range Sum [1-4]: {total_range_sum}")