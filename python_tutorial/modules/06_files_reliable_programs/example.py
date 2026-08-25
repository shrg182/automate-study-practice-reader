import json
from pathlib import Path
from tempfile import TemporaryDirectory

def save(path: Path, record: dict[str, object]) -> None:
    if "title" not in record: raise ValueError("record requires a title")
    path.write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")

if __name__ == "__main__":
    with TemporaryDirectory() as folder:
        path = Path(folder) / "study.json"
        save(path, {"title": "Python", "complete": False})
        print(json.loads(path.read_text(encoding="utf-8")))
