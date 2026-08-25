from typing import Protocol
class Plugin(Protocol):
    name: str
    def transform(self, text: str) -> str: ...
class Uppercase:
    name = "uppercase"
    def transform(self, text): return text.upper()
def apply(plugin: Plugin, text): return plugin.transform(text)
if __name__ == "__main__": print(apply(Uppercase(), "plugin contract"))
