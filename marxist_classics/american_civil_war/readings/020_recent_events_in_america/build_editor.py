#!/usr/bin/env python3
from pathlib import Path
import sys
PROJECT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT.parents[1]))
from build_reading import build  # noqa: E402
if __name__ == "__main__": print(f"Output: {build(PROJECT)}")
