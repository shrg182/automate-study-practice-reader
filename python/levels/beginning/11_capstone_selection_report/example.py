from collections import Counter

def build_report(payload: dict[str, object]) -> dict[str, object]:
    raw = payload.get("selections", [])
    if not isinstance(raw, list): raise ValueError("selections must be a list")
    records = [item for item in raw if isinstance(item, dict)]
    colors = Counter(str(item.get("color", "unlabeled")) for item in records)
    words = sum(len(str(item.get("text", "")).split()) for item in records)
    return {"selection_count": len(records), "word_count": words, "colors": dict(colors)}

if __name__ == "__main__":
    sample = {"selections": [{"text": "Functions return values", "color": "yellow"},
                              {"text": "Validate file input", "color": "blue"}]}
    print(build_report(sample))
