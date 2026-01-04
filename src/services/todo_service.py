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

    def _validate_category(self, category: Optional[str]) -> Optional[str]:
        """Validate and normalize category.

        Args:
            category: Category string to validate

        Returns:
            Normalized category or None
        """
        if category is None:
            return None

        category = category.strip()
        if category == "":
            return None

        return category

    def _validate_tags(self, tags: Optional[List[str]]) -> List[str]:
        """Validate and normalize tags.

        Args:
            tags: List of tag strings to validate

        Returns:
            Normalized list of unique tags
        """
        if tags is None:
            return []

        # Strip whitespace from each tag
        tags = [tag.strip() for tag in tags]

        # Remove empty strings
        tags = [tag for tag in tags if tag]

        # Remove duplicates (case-insensitive)
        seen = set()
        unique_tags = []
        for tag in tags:
            tag_lower = tag.lower()
            if tag_lower not in seen:
                seen.add(tag_lower)
                unique_tags.append(tag)

        return unique_tags

    def add_task(
        self,
        title: str,
        priority: Optional[str] = None,
        due_date: Optional[str] = None,
        category: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> Tuple[Task, Optional[str]]:
        """Add a new task to the list.

        Args:
            title: Task title (required, max 500 chars)
            priority: Priority level (low/medium/high), defaults to medium
            due_date: Due date string (optional, natural language or ISO format)
            category: Optional category (e.g., "work", "personal")
            tags: Optional list of tags (e.g., ["urgent", "bug-fix"])

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

        # Validate category and tags
        validated_category = self._validate_category(category)
        validated_tags = self._validate_tags(tags)

        # Create task
        task = Task(
            id=self._next_id,
            title=title,
            status=TaskStatus.PENDING,
            priority=task_priority,
            created_at=datetime.now(),
            due_date=parsed_due_date,
            category=validated_category,
            tags=validated_tags
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
        due_date: Optional[str] = None,
        category: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> Tuple[Optional[Task], Dict[str, Tuple[str, str]], Optional[str]]:
        """Update a task's title, priority, due date, category, and/or tags.

        Args:
            task_id: The task ID to update
            title: New title (optional)
            priority: New priority (optional)
            due_date: New due date (optional, natural language or ISO format)
            category: New category (optional, use "none" to clear)
            tags: New tags (optional, use ["none"] to clear)

        Returns:
            Tuple of (task, changes dict, error message or None)
            changes dict maps field name to (old_value, new_value)
        """
        task = self.get_task_by_id(task_id)
        if not task:
            return None, {}, f"Task not found (ID: {task_id})"

        if title is None and priority is None and due_date is None and category is None and tags is None:
            return None, {}, "No changes specified. Use --title, --priority, --due, --category, or --tags."

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

        # Update category if provided
        if category is not None:
            old_category = task.category if task.category else "none"
            if category.lower() == "none":
                task.category = None
                new_category = "none"
            else:
                task.category = self._validate_category(category)
                new_category = task.category if task.category else "none"
            if old_category != new_category:
                changes["category"] = (old_category, new_category)

        # Update tags if provided
        if tags is not None:
            old_tags = ", ".join(task.tags) if task.tags else "none"
            if len(tags) == 1 and tags[0].lower() == "none":
                task.tags = []
                new_tags = "none"
            else:
                task.tags = self._validate_tags(tags)
                new_tags = ", ".join(task.tags) if task.tags else "none"
            if old_tags != new_tags:
                changes["tags"] = (old_tags, new_tags)

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

    def get_tasks_by_category(self, category: str) -> List[Task]:
        """Get tasks filtered by category.

        Args:
            category: Category to filter by

        Returns:
            List of matching tasks sorted by ID
        """
        return sorted(
            [t for t in self._tasks.values() if t.category and t.category.lower() == category.lower()],
            key=lambda t: t.id
        )

    def get_tasks_by_tag(self, tag: str) -> List[Task]:
        """Get tasks filtered by tag.

        Args:
            tag: Tag to filter by

        Returns:
            List of matching tasks sorted by ID
        """
        return sorted(
            [t for t in self._tasks.values() if tag.lower() in [t_tag.lower() for t_tag in t.tags]],
            key=lambda t: t.id
        )

    def get_all_categories(self) -> List[str]:
        """Get all unique categories from tasks.

        Returns:
            Sorted list of unique category names
        """
        categories = set()
        for task in self._tasks.values():
            if task.category:
                categories.add(task.category)
        return sorted(categories)

    def get_all_tags(self) -> List[str]:
        """Get all unique tags from tasks.

        Returns:
            Sorted list of unique tag names
        """
        tags = set()
        for task in self._tasks.values():
            tags.update(task.tags)
        return sorted(tags)
