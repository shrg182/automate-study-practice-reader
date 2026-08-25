from statistics import mean, median, pstdev

def reading_report(minutes: list[float]) -> dict[str, float]:
    if not minutes: raise ValueError("at least one session is required")
    return {"sessions": float(len(minutes)), "mean": mean(minutes),
            "median": median(minutes), "spread": pstdev(minutes)}

if __name__ == "__main__":
    for name, value in reading_report([20, 35, 25, 40]).items():
        print(f"{name}: {value:.2f}")
