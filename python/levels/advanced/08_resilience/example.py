def retry(operation, attempts=3):
    error = None
    for _ in range(attempts):
        try: return operation()
        except RuntimeError as caught: error = caught
    raise error
if __name__ == "__main__": print(retry(lambda: "completed"))
