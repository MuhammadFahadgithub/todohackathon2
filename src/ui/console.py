"""Console UI for Todo CLI Core with Rich formatting."""

import sys
import io
from datetime import datetime
from typing import Dict, List, Optional, Tuple

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

from src.models.task import Task, TaskStatus, TaskPriority

# Fix Windows console encoding for unicode characters
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


class ConsoleUI:
    """Handles console output formatting for the Todo CLI with Rich library."""

    def __init__(self):
        """Initialize Rich console."""
        self.console = Console(force_terminal=True)

    def get_priority_color(self, priority: TaskPriority) -> str:
        """Get color for priority level.

        Args:
            priority: Task priority

        Returns:
            Color name for Rich
        """
        colors = {
            TaskPriority.HIGH: "red",
            TaskPriority.MEDIUM: "yellow",
            TaskPriority.LOW: "green"
        }
        return colors.get(priority, "white")

    def get_status_color(self, status: TaskStatus) -> str:
        """Get color for status.

        Args:
            status: Task status

        Returns:
            Color name for Rich
        """
        colors = {
            TaskStatus.PENDING: "cyan",
            TaskStatus.COMPLETED: "green"
        }
        return colors.get(status, "white")

    def format_due_date(self, task: Task) -> Tuple[str, str]:
        """Format the due date with color.

        Args:
            task: The task to format due date for

        Returns:
            Tuple of (formatted date string, color)
        """
        if not task.due_date:
            return "-", "dim"

        now = datetime.now()
        is_overdue = task.due_date < now and task.status == TaskStatus.PENDING

        # Format date
        if task.due_date.year == now.year:
            date_str = task.due_date.strftime("%b %d")
        else:
            date_str = task.due_date.strftime("%b %d, %Y")

        if is_overdue:
            return "⚠ OVERDUE", "red bold"

        # Upcoming soon (within 2 days)
        days_until = (task.due_date - now).days
        if 0 <= days_until <= 2:
            return f"⏰ {date_str}", "yellow"

        return date_str, "white"

    def format_task_created(self, task: Task) -> None:
        """Display a newly created task with Rich formatting.

        Args:
            task: The created task
        """
        text = Text()
        text.append("✅ Created task: ", style="bold green")
        text.append(task.title, style="bold")
        text.append(f" (ID: {task.id})", style="dim")

        self.console.print(text)
        self.console.print(f"   Priority: ", style="dim", end="")
        self.console.print(task.priority.value, style=self.get_priority_color(task.priority))

        if task.due_date:
            self.console.print(f"   Due: ", style="dim", end="")
            due_str, due_color = self.format_due_date(task)
            self.console.print(due_str.replace("⏰ ", "").replace("⚠ ", ""), style=due_color)

        if task.category:
            self.console.print(f"   Category: ", style="dim", end="")
            self.console.print(task.category, style="cyan")

        if task.tags:
            self.console.print(f"   Tags: ", style="dim", end="")
            self.console.print(", ".join(task.tags), style="magenta")

    def format_task_list(self, tasks: List[Task]) -> None:
        """Display a list of tasks in a Rich table.

        Args:
            tasks: List of tasks to display
        """
        # Create table
        table = Table(
            show_header=True,
            header_style="bold cyan",
            border_style="bright_black",
            title="📋 Todo List",
            title_style="bold magenta"
        )

        # Add columns
        table.add_column("ID", justify="right", style="cyan", width=4)
        table.add_column("Status", width=10)
        table.add_column("Priority", width=9)
        table.add_column("Due", width=14)
        table.add_column("Category", width=12)
        table.add_column("Tags", width=20)
        table.add_column("Title", style="white", no_wrap=False)

        # Add rows
        for task in tasks:
            # Format status with icon
            status_icons = {
                TaskStatus.PENDING: "⏳",
                TaskStatus.COMPLETED: "✓"
            }
            status_icon = status_icons.get(task.status, "")
            status_text = f"{status_icon} {task.status.value}"

            # Format priority with color
            priority_text = Text(task.priority.value)
            priority_text.stylize(self.get_priority_color(task.priority))

            # Format due date
            due_str, due_color = self.format_due_date(task)
            due_text = Text(due_str)
            due_text.stylize(due_color)

            # Format category
            category_str = task.category if task.category else "-"
            if len(category_str) > 12:
                category_str = category_str[:9] + "..."

            # Format tags (truncate to 5 tags max)
            if task.tags:
                display_tags = task.tags[:5]
                tags_str = ", ".join(display_tags)
                if len(task.tags) > 5:
                    tags_str += ", ..."
                # Truncate if still too long
                if len(tags_str) > 20:
                    tags_str = tags_str[:17] + "..."
            else:
                tags_str = "-"

            # Format title (truncate if too long)
            title = task.title
            if len(title) > 40:
                title = title[:37] + "..."

            # Add row with color coding
            status_color = self.get_status_color(task.status)
            table.add_row(
                str(task.id),
                Text(status_text, style=status_color),
                priority_text,
                due_text,
                category_str,
                tags_str,
                title
            )

        self.console.print(table)

        # Summary
        pending = sum(1 for t in tasks if t.status == TaskStatus.PENDING)
        completed = len(tasks) - pending
        now = datetime.now()
        overdue = sum(1 for t in tasks if t.due_date and t.due_date < now and t.status == TaskStatus.PENDING)

        summary = Text()
        summary.append("Total: ", style="bold")
        summary.append(f"{len(tasks)} tasks ", style="cyan")
        summary.append(f"({pending} pending, ", style="yellow")
        summary.append(f"{completed} completed", style="green")

        if overdue > 0:
            summary.append(f", ", style="white")
            summary.append(f"{overdue} overdue", style="bold red")

        summary.append(")", style="white")

        self.console.print()
        self.console.print(summary)

    def format_empty_list(self) -> None:
        """Display message when no tasks exist."""
        panel = Panel(
            "[dim]No tasks found.[/dim]\n\n"
            "[cyan]💡 Tip:[/cyan] Add a task with [yellow]'todo add \"Your task title\"'[/yellow]",
            title="📋 Todo List",
            border_style="blue"
        )
        self.console.print(panel)

    def format_task_completed(self, task: Task) -> None:
        """Display a completed task message.

        Args:
            task: The completed task
        """
        text = Text()
        text.append("✅ Completed task: ", style="bold green")
        text.append(task.title, style="bold")
        text.append(f" (ID: {task.id})", style="dim")
        self.console.print(text)

    def format_task_already_completed(self, task: Task) -> None:
        """Display message when task was already completed.

        Args:
            task: The already-completed task
        """
        text = Text()
        text.append("ℹ️  Task already completed: ", style="blue")
        text.append(task.title, style="bold")
        text.append(f" (ID: {task.id})", style="dim")
        self.console.print(text)

    def format_task_updated(self, task: Task, changes: Dict[str, Tuple[str, str]]) -> None:
        """Display an updated task with changes.

        Args:
            task: The updated task
            changes: Dict of field name to (old_value, new_value)
        """
        text = Text()
        text.append("🔄 Updated task ", style="bold cyan")
        text.append(f"(ID: {task.id}):", style="dim")
        self.console.print(text)

        for field, (old_val, new_val) in changes.items():
            change_text = Text()
            change_text.append("  ", style="")
            change_text.append(f"{field.replace('_', ' ').capitalize()}: ", style="dim")
            change_text.append(old_val, style="red strikethrough")
            change_text.append(" → ", style="dim")
            change_text.append(new_val, style="green bold")
            self.console.print(change_text)

    def format_task_deleted(self, task: Task) -> None:
        """Display a deleted task message.

        Args:
            task: The deleted task
        """
        text = Text()
        text.append("🗑️  Deleted task: ", style="bold red")
        text.append(task.title, style="bold")
        text.append(f" (ID: {task.id})", style="dim")
        self.console.print(text)

    def format_categories_list(self, categories: List[str]) -> None:
        """Display a list of all categories in use.

        Args:
            categories: List of unique category names
        """
        if not categories:
            panel = Panel(
                "[dim]No categories in use yet.[/dim]\n\n"
                "[cyan]💡 Tip:[/cyan] Add a category with [yellow]'todo add \"Task\" --category work'[/yellow]",
                title="📂 Categories",
                border_style="cyan"
            )
            self.console.print(panel)
            return

        text = Text()
        text.append(f"📂 Categories ({len(categories)}):\n\n", style="bold magenta")

        for category in categories:
            text.append("  • ", style="dim")
            text.append(category, style="cyan")
            text.append("\n")

        text.append("\n")
        text.append("Use: ", style="dim")
        text.append("todo list --category <name>", style="yellow")

        self.console.print(text)

    def format_tags_list(self, tags: List[str]) -> None:
        """Display a list of all tags in use.

        Args:
            tags: List of unique tag names
        """
        if not tags:
            panel = Panel(
                "[dim]No tags in use yet.[/dim]\n\n"
                "[cyan]💡 Tip:[/cyan] Add tags with [yellow]'todo add \"Task\" --tags urgent important'[/yellow]",
                title="🏷️  Tags",
                border_style="magenta"
            )
            self.console.print(panel)
            return

        text = Text()
        text.append(f"🏷️  Tags ({len(tags)}):\n\n", style="bold magenta")

        for tag in tags:
            text.append("  • ", style="dim")
            text.append(tag, style="magenta")
            text.append("\n")

        text.append("\n")
        text.append("Use: ", style="dim")
        text.append("todo list --tag <name>", style="yellow")

        self.console.print(text)

    def format_error(self, message: str) -> None:
        """Display an error message.

        Args:
            message: The error message
        """
        self.console.print(f"❌ Error: {message}", style="bold red")

    def format_task_not_found(self, task_id: int) -> None:
        """Display a task not found error.

        Args:
            task_id: The ID that was not found
        """
        self.console.print(f"❌ Error: Task not found (ID: {task_id})", style="bold red")

    def format_invalid_id(self, value: str) -> None:
        """Display an invalid ID error.

        Args:
            value: The invalid value provided
        """
        self.console.print(f"❌ Error: Invalid ID '{value}'. Must be a number.", style="bold red")

    def print_success(self, message: str) -> None:
        """Print a success message to stdout.

        Args:
            message: The message to print
        """
        self.console.print(message, style="green")

    def print_error(self, message: str) -> None:
        """Print an error message to stderr.

        Args:
            message: The error message to print
        """
        self.console.print(message, style="bold red", file=sys.stderr)
