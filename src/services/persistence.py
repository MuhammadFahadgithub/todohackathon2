"""Persistence layer for Todo CLI."""

import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from src.models.task import Task, TaskStatus, TaskPriority


class JsonPersistence:
    """JSON file-based persistence for tasks.

    Stores tasks in a JSON file with automatic loading and saving.
    Default location: ~/.todo_cli/tasks.json
    """

    VERSION = "1.0"

    def __init__(self, file_path: Optional[str] = None):
        """Initialize persistence with file path.

        Args:
            file_path: Path to JSON file. Defaults to ~/.todo_cli/tasks.json
        """
        if file_path:
            self.file_path = Path(file_path)
        else:
            self.file_path = Path.home() / ".todo_cli" / "tasks.json"

    def load(self) -> Tuple[Dict[int, Task], int]:
        """Load tasks from JSON file.

        Returns:
            Tuple of (tasks dict, next_id counter)
        """
        if not self.file_path.exists():
            return {}, 1

        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            tasks = {}
            for task_data in data.get("tasks", []):
                task = Task(
                    id=task_data["id"],
                    title=task_data["title"],
                    status=TaskStatus(task_data["status"]),
                    priority=TaskPriority(task_data["priority"]),
                    created_at=datetime.fromisoformat(task_data["created_at"])
                )
                tasks[task.id] = task

            next_id = data.get("next_id", 1)
            return tasks, next_id

        except (json.JSONDecodeError, KeyError, ValueError) as e:
            print(f"Warning: Could not load tasks from {self.file_path}: {e}", file=sys.stderr)
            return {}, 1

    def save(self, tasks: Dict[int, Task], next_id: int) -> bool:
        """Save tasks to JSON file.

        Args:
            tasks: Dictionary of task ID to Task objects
            next_id: Next ID counter value

        Returns:
            True if save successful, False otherwise
        """
        try:
            # Ensure directory exists
            self.file_path.parent.mkdir(parents=True, exist_ok=True)

            # Serialize tasks
            tasks_data = []
            for task in sorted(tasks.values(), key=lambda t: t.id):
                tasks_data.append({
                    "id": task.id,
                    "title": task.title,
                    "status": task.status.value,
                    "priority": task.priority.value,
                    "created_at": task.created_at.isoformat()
                })

            data = {
                "version": self.VERSION,
                "next_id": next_id,
                "tasks": tasks_data
            }

            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)

            return True

        except (IOError, OSError) as e:
            print(f"Warning: Could not save tasks to {self.file_path}: {e}", file=sys.stderr)
            return False
