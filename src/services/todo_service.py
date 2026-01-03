"""Todo service for managing tasks."""

from datetime import datetime, timedelta
from typing import TYPE_CHECKING, Dict, List, Optional, Tuple

from dateutil import parser as date_parser

from src.models.task import Task, TaskStatus, TaskPriority

if TYPE_CHECKING:
    from src.services.persistence import JsonPersistence


def parse_due_date(date_str: str) -> Optional[datetime]:
    """Parse a date string in various formats.

    Args:
        date_str: Date string (e.g., "today", "tomorrow", "2026-01-15", "Jan 15")

    Returns:
        Parsed datetime or None if parsing fails
    """
    if not date_str:
        return None

    date_str_lower = date_str.lower().strip()

    # Handle relative dates
    if date_str_lower == "today":
        parsed = datetime.now()
    elif date_str_lower == "tomorrow":
        parsed = datetime.now() + timedelta(days=1)
    else:
        # Try parsing with dateutil for ISO formats and named dates
        try:
            # First try without fuzzy to catch properly formatted dates
            parsed = date_parser.parse(date_str, fuzzy=False)
        except (ValueError, TypeError, date_parser.ParserError):
            # If that fails, try fuzzy but validate the year is reasonable
            try:
                parsed = date_parser.parse(date_str, fuzzy=True)
                # Reject dates with unrealistic years (before 1900 or more than 100 years in future)
                current_year = datetime.now().year
                if parsed.year < 1900 or parsed.year > current_year + 100:
                    return None
            except (ValueError, TypeError, date_parser.ParserError):
                return None

    # Set time to end of day if no time specified
    if parsed.hour == 0 and parsed.minute == 0 and parsed.second == 0:
        parsed = parsed.replace(hour=23, minute=59, second=59)

    return parsed


class TodoService:
    """Service for CRUD operations on tasks.

    Maintains an in-memory storage of tasks with auto-incrementing IDs.
    Optionally persists to file when persistence layer is provided.
    """

    def __init__(self, persistence: Optional["JsonPersistence"] = None):
        """Initialize the todo service.

        Args:
            persistence: Optional persistence layer for file storage
        """
        self._persistence = persistence
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1

        # Load from persistence if available
        if self._persistence:
            self._tasks, self._next_id = self._persistence.load()

    def _persist(self) -> None:
        """Save current state to persistence layer if available."""
        if self._persistence:
            self._persistence.save(self._tasks, self._next_id)

    def add_task(
        self,
        title: str,
        priority: Optional[str] = None,
        due_date: Optional[str] = None
    ) -> Tuple[Task, Optional[str]]:
        """Add a new task to the list.

        Args:
            title: Task title (required, max 500 chars)
            priority: Priority level (low/medium/high), defaults to medium
            due_date: Due date string (optional, natural language or ISO format)

        Returns:
            Tuple of (created task, error message or None)
        """
        # Validate title
        if not title or not title.strip():
            return None, "Title cannot be empty"

        title = title.strip()
        if len(title) > 500:
            return None, "Title exceeds 500 characters"

        # Validate and parse priority
        task_priority = TaskPriority.MEDIUM
        if priority:
            priority_lower = priority.lower()
            try:
                task_priority = TaskPriority(priority_lower)
            except ValueError:
                return None, f"Invalid priority '{priority}'. Must be: low, medium, high"

        # Parse due date
        parsed_due_date = None
        if due_date:
            parsed_due_date = parse_due_date(due_date)
            if not parsed_due_date:
                return None, f"Invalid due date '{due_date}'. Try: 'today', 'tomorrow', 'Jan 15', or '2026-01-15'"

        # Create task
        task = Task(
            id=self._next_id,
            title=title,
            status=TaskStatus.PENDING,
            priority=task_priority,
            created_at=datetime.now(),
            due_date=parsed_due_date
        )

        self._tasks[self._next_id] = task
        self._next_id += 1
        self._persist()

        return task, None

    def get_all_tasks(self) -> List[Task]:
        """Get all tasks.

        Returns:
            List of all tasks sorted by ID
        """
        return sorted(self._tasks.values(), key=lambda t: t.id)

    def get_tasks_by_status(self, status: str) -> List[Task]:
        """Get tasks filtered by status.

        Args:
            status: Filter value (all/pending/completed)

        Returns:
            List of matching tasks sorted by ID
        """
        if status == "all":
            return self.get_all_tasks()

        try:
            task_status = TaskStatus(status)
            return sorted(
                [t for t in self._tasks.values() if t.status == task_status],
                key=lambda t: t.id
            )
        except ValueError:
            return self.get_all_tasks()

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """Get a task by its ID.

        Args:
            task_id: The task ID to look up

        Returns:
            The task if found, None otherwise
        """
        return self._tasks.get(task_id)

    def complete_task(self, task_id: int) -> Tuple[Optional[Task], bool, Optional[str]]:
        """Mark a task as completed.

        Args:
            task_id: The task ID to complete

        Returns:
            Tuple of (task, was_already_completed, error message or None)
        """
        task = self.get_task_by_id(task_id)
        if not task:
            return None, False, f"Task not found (ID: {task_id})"

        was_already_completed = task.status == TaskStatus.COMPLETED
        task.status = TaskStatus.COMPLETED
        self._persist()

        return task, was_already_completed, None

    def update_task(
        self,
        task_id: int,
        title: Optional[str] = None,
        priority: Optional[str] = None,
        due_date: Optional[str] = None
    ) -> Tuple[Optional[Task], Dict[str, Tuple[str, str]], Optional[str]]:
        """Update a task's title, priority, and/or due date.

        Args:
            task_id: The task ID to update
            title: New title (optional)
            priority: New priority (optional)
            due_date: New due date (optional, natural language or ISO format)

        Returns:
            Tuple of (task, changes dict, error message or None)
            changes dict maps field name to (old_value, new_value)
        """
        task = self.get_task_by_id(task_id)
        if not task:
            return None, {}, f"Task not found (ID: {task_id})"

        if title is None and priority is None and due_date is None:
            return None, {}, "No changes specified. Use --title, --priority, or --due."

        changes = {}

        # Update title if provided
        if title is not None:
            if not title.strip():
                return None, {}, "Title cannot be empty"
            if len(title) > 500:
                return None, {}, "Title exceeds 500 characters"

            old_title = task.title
            task.title = title.strip()
            if old_title != task.title:
                changes["title"] = (old_title, task.title)

        # Update priority if provided
        if priority is not None:
            priority_lower = priority.lower()
            try:
                new_priority = TaskPriority(priority_lower)
                old_priority = task.priority
                task.priority = new_priority
                if old_priority != new_priority:
                    changes["priority"] = (old_priority.value, new_priority.value)
            except ValueError:
                return None, {}, f"Invalid priority '{priority}'. Must be: low, medium, high"

        # Update due date if provided
        if due_date is not None:
            old_due = task.due_date.strftime("%Y-%m-%d") if task.due_date else "none"
            if due_date.lower() in ("none", "clear", ""):
                task.due_date = None
                new_due = "none"
            else:
                parsed = parse_due_date(due_date)
                if not parsed:
                    return None, {}, f"Invalid due date '{due_date}'. Try: 'today', 'tomorrow', 'Jan 15', or '2026-01-15'"
                task.due_date = parsed
                new_due = parsed.strftime("%Y-%m-%d")
            if old_due != new_due:
                changes["due_date"] = (old_due, new_due)

        if changes:
            self._persist()

        return task, changes, None

    def delete_task(self, task_id: int) -> Tuple[Optional[Task], Optional[str]]:
        """Delete a task.

        Args:
            task_id: The task ID to delete

        Returns:
            Tuple of (deleted task, error message or None)
        """
        task = self.get_task_by_id(task_id)
        if not task:
            return None, f"Task not found (ID: {task_id})"

        del self._tasks[task_id]
        self._persist()
        return task, None
