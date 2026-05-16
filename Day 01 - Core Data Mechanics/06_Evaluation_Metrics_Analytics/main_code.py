"""
CORE CONCEPT: Core Binary Metrics Evaluation Engine
Constructing a low-level validation system that calculates classification metrics 
directly from target labels. Computes True/False matrices from scratch to derive Precision, 
Recall, and F1-Scores.
"""

class BinaryClassificationEvaluator:
    @staticmethod
    def calculate_metrics(actual: list[int], predicted: list[int]) -> dict[str, float]:
        """Evaluates prediction arrays against labels to generate classification metrics."""
        if len(actual) != len(predicted) or len(actual) == 0:
            raise ValueError("Target validation matrices must remain aligned and non-empty.")

        tp = tn = fp = fn = 0

        # Build confusion matrix counts
        for act, pred in zip(actual, predicted):
            if act == 1 and pred == 1:
                tp += 1
            elif act == 0 and pred == 0:
                tn += 1
            elif act == 0 and pred == 1:
                fp += 1
            elif act == 1 and pred == 0:
                fn += 1

        precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1_score = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0

        return {
            "True_Positives": tp,
            "False_Positives": fp,
            "True_Negatives": tn,
            "False_Negatives": fn,
            "Precision": round(precision, 4),
            "Recall": round(recall, 4),
            "F1_Score": round(f1_score, 4)
        }


if __name__ == "__main__":
    targets     = [1, 0, 1, 1, 0, 0, 1, 0]
    predictions = [1, 0, 0, 1, 1, 0, 1, 0]
    
    analytics = BinaryClassificationEvaluator.calculate_metrics(targets, predictions)
    for matrix_key, evaluation_score in analytics.items():
        print(f"{matrix_key}: {evaluation_score}")