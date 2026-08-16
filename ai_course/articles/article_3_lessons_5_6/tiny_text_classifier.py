#!/usr/bin/env python3
"""A tiny, inspectable multinomial naive Bayes text classifier."""

from __future__ import annotations

from collections import Counter, defaultdict
from math import log
import re


TRAINING_DATA = [
    ("review the chapter before class", "study"),
    ("practice vocabulary for the quiz", "study"),
    ("organize lecture notes tonight", "study"),
    ("finish the reading assignment", "study"),
    ("buy fruit on the way home", "everyday"),
    ("cook dinner and wash dishes", "everyday"),
    ("pick up a package from the store", "everyday"),
    ("do the laundry this evening", "everyday"),
]

TEST_DATA = [
    ("study the notes for tomorrow's quiz", "study"),
    ("complete the chapter reading", "study"),
    ("buy groceries for dinner", "everyday"),
    ("wash clothes after work", "everyday"),
]


def tokenize(text: str) -> list[str]:
    """Return lowercase word tokens from a short message."""
    return re.findall(r"[a-z]+(?:'[a-z]+)?", text.lower())


class NaiveBayesClassifier:
    """Minimal multinomial naive Bayes with Laplace smoothing."""

    def __init__(self) -> None:
        self.category_documents: Counter[str] = Counter()
        self.word_counts: dict[str, Counter[str]] = defaultdict(Counter)
        self.total_words: Counter[str] = Counter()
        self.vocabulary: set[str] = set()

    def fit(self, examples: list[tuple[str, str]]) -> None:
        for text, category in examples:
            words = tokenize(text)
            self.category_documents[category] += 1
            self.word_counts[category].update(words)
            self.total_words[category] += len(words)
            self.vocabulary.update(words)

    def scores(self, text: str) -> dict[str, float]:
        if not self.category_documents:
            raise RuntimeError("Call fit() before predict().")
        document_count = sum(self.category_documents.values())
        vocabulary_size = len(self.vocabulary)
        results: dict[str, float] = {}
        for category, category_count in self.category_documents.items():
            score = log(category_count / document_count)
            denominator = self.total_words[category] + vocabulary_size
            for word in tokenize(text):
                score += log((self.word_counts[category][word] + 1) / denominator)
            results[category] = score
        return results

    def predict(self, text: str) -> str:
        category_scores = self.scores(text)
        return max(category_scores, key=category_scores.get)


def evaluate(model: NaiveBayesClassifier) -> tuple[int, int]:
    correct = sum(model.predict(text) == expected for text, expected in TEST_DATA)
    return correct, len(TEST_DATA)


def main() -> None:
    model = NaiveBayesClassifier()
    model.fit(TRAINING_DATA)

    examples = [
        "review notes before the quiz",
        "pick up dinner from the store",
        "finish laundry and then read the chapter",
    ]
    print("Predictions")
    for message in examples:
        score_text = ", ".join(
            f"{category}={score:.2f}"
            for category, score in sorted(model.scores(message).items())
        )
        print(f"- {message!r} -> {model.predict(message)} ({score_text})")

    correct, total = evaluate(model)
    print(f"\nHeld-out test accuracy: {correct}/{total} = {correct / total:.0%}")


if __name__ == "__main__":
    main()
