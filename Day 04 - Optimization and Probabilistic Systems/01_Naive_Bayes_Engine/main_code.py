"""
CORE CONCEPT: Naive Bayes Statistical Engine
Building a pure object-oriented text classifier based on Bayes' Theorem.
Implements prior calculation, word token log-likelihood computation, and 
Laplace smoothing to prevent zero-probability dropouts.
"""

import math
from collections import Counter, defaultdict

class NaiveBayesClassifier:
    def __init__(self, alpha: float = 1.0):
        self.alpha = alpha  # Laplace smoothing parameter
        self.class_counts = Counter()
        self.feature_counts = defaultdict(Counter)
        self.class_total_words = Counter()
        self.vocabulary = set()

    def train(self, training_data: list[tuple[list[str], str]]) -> None:
        """Processes tokenized inputs to update prior frequency matrices and vocab maps."""
        for tokens, label in training_data:
            self.class_counts[label] += 1
            for token in tokens:
                self.feature_counts[label][token] += 1
                self.class_total_words[label] += 1
                self.vocabulary.add(token)

    def predict(self, tokens: list[str]) -> str:
        """Evaluates conditional token logs using Bayes' Theorem to find the argmax label."""
        total_documents = sum(self.class_counts.values())
        best_label = None
        highest_log_prob = -float('inf')
        vocab_size = len(self.vocabulary)

        for label, count in self.class_counts.items():
            # Calculate Prior: P(Class)
            log_probability = math.log(count / total_documents)

            # Accumulate Likelihoods: P(Word | Class) using log space to prevent underflow
            for token in tokens:
                if token in self.vocabulary:
                    word_count = self.feature_counts[label][token]
                    # Apply Laplace Smoothing formula
                    smoothed_likelihood = (word_count + self.alpha) / (self.class_total_words[label] + self.alpha * vocab_size)
                    log_probability += math.log(smoothed_likelihood)

            if log_probability > highest_log_prob:
                highest_log_prob = log_probability
                best_label = label

        return best_label if best_label else "Unknown"


if __name__ == "__main__":
    # Mock data layout: (Tokenized text array, Category)
    corpus = [
        (["prize", "money", "claim", "now"], "Spam"),
        (["urgent", "award", "win", "cash"], "Spam"),
        (["meeting", "project", "schedule", "tomorrow"], "Ham"),
        (["team", "lunch", "agenda", "discussion"], "Ham")
    ]

    classifier = NaiveBayesClassifier(alpha=1.0)
    classifier.train(corpus)

    test_sample = ["claim", "urgent", "cash"]
    prediction = classifier.predict(test_sample)
    print(f"Tokenized Sample Class Verification Result: {prediction}")