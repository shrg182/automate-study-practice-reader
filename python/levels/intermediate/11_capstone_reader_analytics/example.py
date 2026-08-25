import json

def summarize(raw):
    data = json.loads(raw); rows = data.get("selections", [])
    if not isinstance(rows, list): raise ValueError("selections must be a list")
    return {"count": len(rows), "characters": sum(len(str(x.get("text", ""))) for x in rows if isinstance(x, dict))}
if __name__ == "__main__": print(summarize('{"selections":[{"text":"Python"}]}'))
