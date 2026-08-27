def summarize(values: list[float]) -> dict[str, float]:
    """Return statistics for a non-empty list."""
    if not values: raise ValueError("values must not be empty")
    return {"minimum": min(values), "maximum": max(values),
            "average": sum(values) / len(values)}

if __name__ == "__main__":
    print(summarize([4.0, 7.5, 8.5]))
