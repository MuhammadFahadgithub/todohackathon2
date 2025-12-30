from typing import List, Optional
from src.models.task import Task
from src.utils.ids import IDGenerator

class TaskService:
    def __init__(self):
        self._tasks: List[Task] = []

    def add_task(self, title: str, description: str = "") -> Task:
        task = Task(id=IDGenerator.next_id(), title=title, description=description)
        self._tasks.append(task)
        return task

    def list_tasks(self) -> List[Task]:
        return self._tasks

    def toggle_task(self, task_id: int) -> Task:
        for i, task in enumerate(self._tasks):
            if task.id == task_id:
                new_task = Task(
                    id=task.id,
                    title=task.title,
                    description=task.description,
                    is_completed=not task.is_completed
                )
                self._tasks[i] = new_task
                return new_task
        raise KeyError(f"Task with ID {task_id} not found.")

    def delete_task(self, task_id: int) -> None:
        for i, task in enumerate(self._tasks):
            if task.id == task_id:
                self._tasks.pop(i)
                return
        raise KeyError(f"Task with ID {task_id} not found.")

    def update_task(self, task_id: int, title: Optional[str] = None, description: Optional[str] = None) -> Task:
        for i, task in enumerate(self._tasks):
            if task.id == task_id:
                new_title = title if title is not None else task.title
                new_desc = description if description is not None else task.description

                new_task = Task(
                    id=task.id,
                    title=new_title,
                    description=new_desc,
                    is_completed=task.is_completed
                )
                self._tasks[i] = new_task
                return new_task
        raise KeyError(f"Task with ID {task_id} not found.")
