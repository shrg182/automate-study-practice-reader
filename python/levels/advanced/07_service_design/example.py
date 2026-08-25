from dataclasses import dataclass

@dataclass(frozen=True)
class Request:
    text: str
def handle(request):
    if not request.text.strip(): return {"status": 400, "error": "text required"}
    return {"status": 200, "words": len(request.text.split())}
if __name__ == "__main__": print(handle(Request("typed service boundary")))
