from contextlib import contextmanager

@contextmanager
def study_session(name):
    print(f"start: {name}")
    try: yield
    finally: print(f"finish: {name}")

if __name__ == "__main__":
    with study_session("typing"): print("practice")
