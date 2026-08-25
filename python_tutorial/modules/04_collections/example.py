import re

def word_frequencies(text: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for word in re.findall(r"[A-Za-z']+", text.lower()):
        counts[word] = counts.get(word, 0) + 1
    return counts

if __name__ == "__main__":
    print(sorted(word_frequencies("Read code, run code, explain code.").items()))
