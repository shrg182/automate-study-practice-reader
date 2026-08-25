def classify_scores(scores: list[int]) -> dict[str, int]:
    result = {"mastered": 0, "review": 0, "retry": 0}
    for score in scores:
        if score >= 85: result["mastered"] += 1
        elif score >= 60: result["review"] += 1
        else: result["retry"] += 1
    return result

if __name__ == "__main__":
    print(classify_scores([92, 74, 58, 85, 61]))
