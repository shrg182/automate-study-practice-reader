from collections import defaultdict

def totals(rows):
    result = defaultdict(int)
    for row in rows: result[row["topic"]] += row["minutes"]
    return dict(result)

if __name__ == "__main__": print(totals([{"topic":"Python","minutes":20},{"topic":"Python","minutes":15}]))
