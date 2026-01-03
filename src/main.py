"""CLI entry point for Todo CLI Core."""

import argparse
import sys
from typing import Optional

from src import __version__
from src.services.persistence import JsonPersistence
from src.services.todo_service import TodoService
from src.ui.console import ConsoleUI


# Global service instance with file persistence
persistence = JsonPersistence()  # ~/.todo_cli/tasks.json
todo_service = TodoService(persistence=persistence)
ui = ConsoleUI()


def parse_task_id(value: str) -> Optional[int]:
    """Parse and validate a task ID.

    Args:
        value: The string value to parse

    Returns:
        The parsed integer ID, or None if invalid
    """
    try:
        return int(value)
    except ValueError:
        return None


def cmd_add(args: argparse.Namespace) -> int:
    """Handle the 'add' subcommand.

    Args:
        args: Parsed command line arguments

    Returns:
        Exit code (0 for success, 1 for error)
    """
    task, error = todo_service.add_task(args.title, args.priority, args.due)

    if error:
        ui.print_error(ui.format_error(error))
        return 1

    ui.print_success(ui.format_task_created(task))
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    """Handle the 'list' subcommand.

    Args:
        args: Parsed command line arguments

    Returns:
        Exit code (0 for success)
    """
    status_filter = getattr(args, 'status', 'all') or 'all'
    tasks = todo_service.get_tasks_by_status(status_filter)

    if not tasks:
        ui.print_success(ui.format_empty_list())
    else:
        ui.print_success(ui.format_task_list(tasks))

    return 0


def cmd_complete(args: argparse.Namespace) -> int:
    """Handle the 'complete' subcommand.

    Args:
        args: Parsed command line arguments

    Returns:
        Exit code (0 for success, 1 for error)
    """
    task_id = parse_task_id(args.id)
    if task_id is None:
        ui.print_error(ui.format_invalid_id(args.id))
        return 1

    task, was_already_completed, error = todo_service.complete_task(task_id)

    if error:
        ui.print_error(ui.format_error(error))
        return 1

    if was_already_completed:
        ui.print_success(ui.format_task_already_completed(task))
    else:
        ui.print_success(ui.format_task_completed(task))

    return 0


def cmd_update(args: argparse.Namespace) -> int:
    """Handle the 'update' subcommand.

    Args:
        args: Parsed command line arguments

    Returns:
        Exit code (0 for success, 1 for error)
    """
    task_id = parse_task_id(args.id)
    if task_id is None:
        ui.print_error(ui.format_invalid_id(args.id))
        return 1

    task, changes, error = todo_service.update_task(
        task_id,
        title=args.title,
        priority=args.priority,
        due_date=args.due
    )

    if error:
        ui.print_error(ui.format_error(error))
        return 1

    if changes:
        ui.print_success(ui.format_task_updated(task, changes))
    else:
        ui.print_success(f"No changes made to task (ID: {task_id})")

    return 0


def cmd_delete(args: argparse.Namespace) -> int:
    """Handle the 'delete' subcommand.

    Args:
        args: Parsed command line arguments

    Returns:
        Exit code (0 for success, 1 for error)
    """
    task_id = parse_task_id(args.id)
    if task_id is None:
        ui.print_error(ui.format_invalid_id(args.id))
        return 1

    task, error = todo_service.delete_task(task_id)

    if error:
        ui.print_error(ui.format_error(error))
        return 1

    ui.print_success(ui.format_task_deleted(task))
    return 0


def create_parser() -> argparse.ArgumentParser:
    """Create the argument parser with all subcommands.

    Returns:
        Configured argument parser
    """
    parser = argparse.ArgumentParser(
        prog="todo",
        description="A simple command-line todo application"
    )
    parser.add_argument(
        "--version", "-v",
        action="version",
        version=f"%(prog)s {__version__}"
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("title", help="Task title (max 500 characters)")
    add_parser.add_argument(
        "--priority", "-p",
        choices=["low", "medium", "high"],
        default="medium",
        help="Task priority (default: medium)"
    )
    add_parser.add_argument(
        "--due", "-d",
        help="Due date (e.g., 'tomorrow', 'next friday', '2026-01-15')"
    )
    add_parser.set_defaults(func=cmd_add)

    # List command
    list_parser = subparsers.add_parser("list", help="List all tasks")
    list_parser.add_argument(
        "--status", "-s",
        choices=["all", "pending", "completed"],
        default="all",
        help="Filter by status (default: all)"
    )
    list_parser.set_defaults(func=cmd_list)

    # Complete command
    complete_parser = subparsers.add_parser("complete", help="Mark a task as completed")
    complete_parser.add_argument("id", help="Task ID to complete")
    complete_parser.set_defaults(func=cmd_complete)

    # Update command
    update_parser = subparsers.add_parser("update", help="Update a task")
    update_parser.add_argument("id", help="Task ID to update")
    update_parser.add_argument(
        "--title", "-t",
        help="New task title"
    )
    update_parser.add_argument(
        "--priority", "-p",
        choices=["low", "medium", "high"],
        help="New task priority"
    )
    update_parser.add_argument(
        "--due", "-d",
        help="New due date (e.g., 'tomorrow', 'Jan 15', '2026-01-15', or 'none' to clear)"
    )
    update_parser.set_defaults(func=cmd_update)

    # Delete command
    delete_parser = subparsers.add_parser("delete", help="Delete a task")
    delete_parser.add_argument("id", help="Task ID to delete")
    delete_parser.set_defaults(func=cmd_delete)

    return parser


def main() -> int:
    """Main entry point for the CLI.

    Returns:
        Exit code
    """
    parser = create_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 0

    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
