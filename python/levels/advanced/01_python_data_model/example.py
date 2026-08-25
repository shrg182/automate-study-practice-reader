class Positive:
    def __set_name__(self, owner, name): self.name = "_" + name
    def __get__(self, obj, owner): return getattr(obj, self.name)
    def __set__(self, obj, value):
        if value <= 0: raise ValueError("must be positive")
        setattr(obj, self.name, value)
class Task:
    minutes = Positive()
    def __init__(self, minutes): self.minutes = minutes
if __name__ == "__main__": print(Task(25).minutes)
