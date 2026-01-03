# Quickstart: Todo CLI Core

**Feature**: 001-todo-cli-core
**Date**: 2026-01-02

## Prerequisites

- Python 3.11 or higher
- No additional dependencies required

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd todohackathon2

# Verify Python version
python --version  # Should be 3.11+
```

## Running the Application

```bash
# Run from repository root
python -m src.main <command> [options]
```

## Quick Examples

### Add Tasks

```bash
# Add a simple task
python -m src.main add "Buy groceries"
# Output: Created task: Buy groceries (ID: 1)

# Add a high-priority task
python -m src.main add "Finish report" --priority high
# Output: Created task: Finish report (ID: 2)

# Add a low-priority task
python -m src.main add "Clean desk" -p low
# Output: Created task: Clean desk (ID: 3)
```

### List Tasks

```bash
# List all tasks
python -m src.main list
# Output:
# ID    Status      Priority   Title
# ----  ----------  ---------  --------------------------------------------------
# 1     pending     medium     Buy groceries
# 2     pending     high       Finish report
# 3     pending     low        Clean desk
#
# Total: 3 tasks (3 pending, 0 completed)

# List only pending tasks
python -m src.main list --status pending

# List only completed tasks
python -m src.main list -s completed
```

### Complete Tasks

```bash
# Mark task as complete
python -m src.main complete 1
# Output: Completed task: Buy groceries (ID: 1)

# Verify completion
python -m src.main list
# Task 1 now shows status: completed
```

### Update Tasks

```bash
# Update task title
python -m src.main update 2 --title "Finish quarterly report"
# Output: Updated task (ID: 2):
#   Title: Finish report → Finish quarterly report

# Update task priority
python -m src.main update 3 --priority medium
# Output: Updated task (ID: 3):
#   Priority: low → medium

# Update both
python -m src.main update 2 -t "Submit quarterly report" -p high
```

### Delete Tasks

```bash
# Delete a task
python -m src.main delete 3
# Output: Deleted task: Clean desk (ID: 3)
```

## Common Workflows

### Daily Task Management

```bash
# Morning: Add today's tasks
python -m src.main add "Review emails" -p high
python -m src.main add "Team standup meeting"
python -m src.main add "Code review for PR #42"

# Throughout day: Check and complete
python -m src.main list -s pending
python -m src.main complete 1
python -m src.main complete 2

# End of day: Review progress
python -m src.main list
```

### Prioritizing Work

```bash
# Add tasks with priorities
python -m src.main add "Fix critical bug" -p high
python -m src.main add "Write documentation" -p low
python -m src.main add "Attend meeting" -p medium

# Change priority if needed
python -m src.main update 2 -p high  # Documentation now urgent!
```

## Error Handling

```bash
# Empty title (rejected)
python -m src.main add ""
# Error: Title cannot be empty

# Invalid task ID
python -m src.main complete 999
# Error: Task not found (ID: 999)

# Invalid priority
python -m src.main add "Task" -p urgent
# Error: Invalid priority 'urgent'. Must be: low, medium, high
```

## Getting Help

```bash
# General help
python -m src.main --help

# Command-specific help
python -m src.main add --help
python -m src.main list --help
```

## Notes

- **Data Persistence**: Tasks are stored in memory only. Data is lost when the application exits. This is expected behavior for Phase 1.
- **Single User**: The application is designed for single-user, local use.
- **Task IDs**: IDs are assigned sequentially starting from 1 and never reused within a session.

## Running Tests

```bash
# Install pytest (if not already installed)
pip install pytest

# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/unit/test_todo_service.py
```
