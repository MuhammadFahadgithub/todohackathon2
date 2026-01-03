"""Task model for Todo CLI Core."""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional


class TaskStatus(Enum):
    """Status of a task."""
    PENDING = "pending"
    COMPLETED = "completed"


class TaskPriority(Enum):
    """Priority level of a task."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass
class Task:
    """Represents a single todo item.

    Attributes:
        id: Unique identifier for the task
        title: Task title (max 500 characters)
        status: Current status (pending/completed)
        priority: Priority level (low/medium/high)
        created_at: Timestamp when task was created
        due_date: Optional due date for the task
    """
    id: int
    title: str
    status: TaskStatus = TaskStatus.PENDING
    priority: TaskPriority = TaskPriority.MEDIUM
    created_at: datetime = field(default_factory=datetime.now)
    due_date: Optional[datetime] = None

    def __post_init__(self):
        """Validate task after initialization."""
        if not self.title or not self.title.strip():
            raise ValueError("Title cannot be empty")
        if len(self.title) > 500:
            raise ValueError("Title exceeds 500 characters")
