from dataclasses import dataclass

@dataclass(frozen=True)
class Task:
    id: int
    title: str
    description: str = ""
    is_completed: bool = False

    def __post_init__(self):
        if not self.title or not self.title.strip():
            raise ValueError("Task title cannot be empty.")
