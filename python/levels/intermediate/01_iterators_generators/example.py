def batched(source, size):
    batch = []
    for item in source:
        batch.append(item)
        if len(batch) == size:
            yield tuple(batch); batch.clear()
    if batch: yield tuple(batch)

if __name__ == "__main__": print(list(batched(range(7), 3)))
