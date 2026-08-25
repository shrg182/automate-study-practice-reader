from dataclasses import dataclass

@dataclass
class StudyItem:
    title: str
    minutes: int
    reviewed: bool = False
    def mark_reviewed(self) -> None: self.reviewed = True
    def label(self) -> str:
        return f"[{'done' if self.reviewed else 'next'}] {self.title} ({self.minutes} min)"

if __name__ == "__main__":
    item = StudyItem("Functions", 25)
    print(item.label()); item.mark_reviewed(); print(item.label())
