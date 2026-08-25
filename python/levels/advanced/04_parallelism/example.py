from concurrent.futures import ThreadPoolExecutor

def square(value): return value * value
if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=3) as pool: print(list(pool.map(square, range(6))))
