"""Console UI for Todo CLI Core."""

import sys
from typing import Dict, List, Optional, Tuple

from src.models.task import Task


class ConsoleUI:
    """Handles console output formatting for the Todo CLI."""

    # Column widths for list output
    ID_WIDTH = 4
    STATUS_WIDTH = 10
    PRIORITY_WIDTH = 9
    TITLE_WIDTH = 50

    @staticmethod
    def format_task_created(task: Task) -> str:
        """Format output for a newly created task.

        Args:
            task: The created task

        Returns:
            Formatted success message
        """
        return (
            f"Created task: {task.title} (ID: {task.id})\n"
            f"Priority: {task.priority.value}"
        )

    @staticmethod
    def format_task_list(tasks: List[Task]) -> str:
        """Format a list of tasks with aligned columns.

        Args:
            tasks: List of tasks to display

        Returns:
            Formatted task table
        """
        # Header
        header = (
            f"{'ID':<{ConsoleUI.ID_WIDTH}}  "
            f"{'Status':<{ConsoleUI.STATUS_WIDTH}}  "
            f"{'Priority':<{ConsoleUI.PRIORITY_WIDTH}}  "
            f"{'Title':<{ConsoleUI.TITLE_WIDTH}}"
        )
        separator = (
            f"{'-' * ConsoleUI.ID_WIDTH}  "
            f"{'-' * ConsoleUI.STATUS_WIDTH}  "
            f"{'-' * ConsoleUI.PRIORITY_WIDTH}  "
            f"{'-' * ConsoleUI.TITLE_WIDTH}"
        )

        lines = [header, separator]

        # Task rows
        for task in tasks:
            title = task.title
            if len(title) > ConsoleUI.TITLE_WIDTH:
                title = title[:ConsoleUI.TITLE_WIDTH - 3] + "..."

            line = (
                f"{task.id:<{ConsoleUI.ID_WIDTH}}  "
                f"{task.status.value:<{ConsoleUI.STATUS_WIDTH}}  "
                f"{task.priority.value:<{ConsoleUI.PRIORITY_WIDTH}}  "
                f"{title:<{ConsoleUI.TITLE_WIDTH}}"
            )
            lines.append(line)

        # Summary
        pending = sum(1 for t in tasks if t.status.value == "pending")
        completed = len(tasks) - pending
        lines.append("")
        lines.append(f"Total: {len(tasks)} tasks ({pending} pending, {completed} completed)")

        return "\n".join(lines)

    @staticmethod
    def format_empty_list() -> str:
        """Format output when no tasks exist.

        Returns:
            Friendly empty list message with tip
        """
        return (
            "No tasks found.\n\n"
            "Tip: Add a task with 'todo add \"Your task title\"'"
        )

    @staticmethod
    def format_task_completed(task: Task) -> str:
        """Format output for a completed task.

        Args:
            task: The completed task

        Returns:
            Formatted success message
        """
        return f"Completed task: {task.title} (ID: {task.id})"

    @staticmethod
    def format_task_already_completed(task: Task) -> str:
        """Format output when task was already completed.

        Args:
            task: The already-completed task

        Returns:
            Formatted informational message
        """
        return f"Task already completed: {task.title} (ID: {task.id})"

    @staticmethod
    def format_task_updated(task: Task, changes: Dict[str, Tuple[str, str]]) -> str:
        """Format output for an updated task.

        Args:
            task: The updated task
            changes: Dict of field name to (old_value, new_value)

        Returns:
            Formatted success message showing changes
        """
        lines = [f"Updated task (ID: {task.id}):"]
        for field, (old_val, new_val) in changes.items():
            lines.append(f"  {field.capitalize()}: {old_val} -> {new_val}")
        return "\n".join(lines)

    @staticmethod
    def format_task_deleted(task: Task) -> str:
        """Format output for a deleted task.

        Args:
            task: The deleted task

        Returns:
            Formatted success message
        """
        return f"Deleted task: {task.title} (ID: {task.id})"

    @staticmethod
    def format_error(message: str) -> str:
        """Format an error message.

        Args:
            message: The error message

        Returns:
            Formatted error string
        """
        return f"Error: {message}"

    @staticmethod
    def format_task_not_found(task_id: int) -> str:
        """Format a task not found error.

        Args:
            task_id: The ID that was not found

        Returns:
            Formatted error message
        """
        return f"Error: Task not found (ID: {task_id})"

    @staticmethod
    def format_invalid_id(value: str) -> str:
        """Format an invalid ID error.

        Args:
            value: The invalid value provided

        Returns:
            Formatted error message
        """
        return f"Error: Invalid ID '{value}'. Must be a number."

    @staticmethod
    def print_success(message: str) -> None:
        """Print a success message to stdout.

        Args:
            message: The message to print
        """
        print(message)

    @staticmethod
    def print_error(message: str) -> None:
        """Print an error message to stderr.

        Args:
            message: The error message to print
        """
        print(message, file=sys.stderr)
