from typing import Generic, TypeVar
T = TypeVar("T")
class Stack(Generic[T]):
    def __init__(self): self._items: list[T] = []
    def push(self, item: T) -> None: self._items.append(item)
    def pop(self) -> T: return self._items.pop()
if __name__ == "__main__":
    stack = Stack[str](); stack.push("types"); print(stack.pop())
