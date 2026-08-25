import platform
import sys

def runtime_report() -> dict[str, str]:
    return {"python": platform.python_version(),
            "implementation": platform.python_implementation(),
            "executable": sys.executable}

if __name__ == "__main__":
    for key, value in runtime_report().items(): print(f"{key}: {value}")
