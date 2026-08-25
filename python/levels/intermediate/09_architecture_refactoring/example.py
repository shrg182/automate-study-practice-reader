def completion(done, total):
    if total <= 0: raise ValueError("total must be positive")
    return done / total

def format_completion(value): return f"{value:.0%} complete"
if __name__ == "__main__": print(format_completion(completion(7, 10)))
