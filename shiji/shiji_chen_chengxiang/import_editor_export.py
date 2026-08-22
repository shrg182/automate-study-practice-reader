#!/usr/bin/env python3
"""Promote a Chen Chengxiang editor backup using the shared Shiji importer."""
from pathlib import Path
import shutil
import sys

BASE_DIR = Path(__file__).resolve().parent
SHARED_DIR = BASE_DIR.parent / "shiji_lisheng_lujia"
sys.path.insert(0, str(SHARED_DIR))

import import_editor_export as shared  # noqa: E402

if __name__ == "__main__":
    if len(sys.argv) > 1 and not sys.argv[1].startswith("-"):
        shutil.copyfile(Path(sys.argv[1]), BASE_DIR / "chen_chengxiang_editor_seed.json")
    shared.BASE_DIR = BASE_DIR
    shared.main()
