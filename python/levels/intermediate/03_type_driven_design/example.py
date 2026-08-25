from dataclasses import dataclass
from typing import Protocol

class Renderable(Protocol):
    def render(self) -> str: ...

@dataclass
class Note:
    text: str
    def render(self) -> str: return f"- {self.text}"

def publish(item: Renderable) -> str: return item.render()
if __name__ == "__main__": print(publish(Note("Review protocols")))
