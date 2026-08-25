import platform
import sys

def environment_summary() -> str:
    return f"Python {platform.python_version()} at {sys.executable}"

if __name__ == "__main__":
    print("Hello, Python learner!")
    print(environment_summary())
