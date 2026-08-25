def bars(values, width=20):
    largest = max(values.values(), default=1)
    return "
".join(f"{name:10} {'#' * round(value/largest*width)} {value}" for name, value in values.items())
if __name__ == "__main__": print(bars({"reading": 30, "coding": 45, "testing": 15}))
