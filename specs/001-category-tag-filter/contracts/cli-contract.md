# CLI Contract: Category and Tag Filtering

**Feature**: 001-category-tag-filter
**Created**: 2026-01-04
**Status**: Design Complete

## Overview

This document specifies the command-line interface contract for category and tag filtering functionality. All commands use argparse for argument parsing and follow existing CLI conventions.

## Command Extensions

### 1. `todo add` - Create Task with Category/Tags

**Signature**:
```bash
todo add <title> [--priority <level>] [--due <date>] [--category <name>] [--tags <tag1> <tag2> ...]
```

**New Arguments**:

| Argument | Short | Type | Required | Default | Description |
|----------|-------|------|----------|---------|-------------|
| --category | -c | str | No | None | Task category (single value) |
| --tags | -t | list[str] | No | [] | Task tags (space-separated) |

**Examples**:
```bash
# Add task with category
todo add "Review PR" --category work --priority high

# Add task with tags
todo add "Fix bug" --tags urgent bug-fix

# Add task with both
todo add "Team meeting" --category work --tags meeting important

# Add task with multi-word category (quoted)
todo add "Doctor appointment" --category "personal health"

# Add task with tags containing spaces (quoted)
todo add "High priority task" --tags "high priority" urgent
```

**Validation**:
- Category: Strip whitespace, empty string → None
- Tags: Strip each tag, remove empty strings, deduplicate case-insensitively
- No special character restrictions (user responsibility)

**Output**:
```
✅ Task created successfully!

[Task details with category and tags displayed]
```

**Error Cases**:
- Invalid priority/due date: Existing error handling applies
- No special errors for category/tags (any string accepted)

---

### 2. `todo update` - Update Task Category/Tags

**Signature**:
```bash
todo update <id> [--title <text>] [--priority <level>] [--due <date>] [--category <name>] [--tags <tag1> <tag2> ...]
```

**New Arguments**:

| Argument | Short | Type | Required | Default | Description |
|----------|-------|------|----------|---------|-------------|
| --category | -c | str | No | (unchanged) | New category or "none" to clear |
| --tags | -t | list[str] | No | (unchanged) | Replace all tags or "none" to clear |

**Examples**:
```bash
# Update category
todo update 5 --category personal

# Clear category
todo update 5 --category none

# Replace tags
todo update 5 --tags review code urgent

# Clear tags
todo update 5 --tags none

# Update multiple fields including category
todo update 5 --priority high --category work --tags urgent
```

**Special Values**:
- `--category none`: Clears category (sets to None)
- `--tags none`: Clears all tags (sets to empty list)
- Case-insensitive: "none", "None", "NONE" all work

**Validation**:
- Same validation as `add` command
- "none" (case-insensitive) is reserved keyword for clearing

**Output**:
```
✅ Task updated successfully!

Changes:
  Category: personal → work
  Tags: [review, code] → [urgent, bug-fix]

[Updated task details displayed]
```

**Error Cases**:
- Task not found: "Error: Task with ID 5 not found"
- Invalid ID: "Error: Invalid task ID"

---

### 3. `todo list` - Filter Tasks by Category/Tag

**Signature**:
```bash
todo list [--status <status>] [--priority <level>] [--category <name>] [--tag <name>]
```

**New Arguments**:

| Argument | Short | Type | Required | Default | Description |
|----------|-------|------|----------|---------|-------------|
| --category | -c | str | No | None | Filter by category (case-insensitive) |
| --tag | -t | str | No | None | Filter by tag (case-insensitive) |

**Examples**:
```bash
# List all work tasks
todo list --category work

# List all urgent tasks
todo list --tag urgent

# Combine with existing filters
todo list --status pending --category work

# Combine category and tag (P3 - requires both)
todo list --category work --tag urgent

# Case-insensitive filtering
todo list --category Work  # Matches "work", "Work", "WORK"
```

**Filtering Behavior**:

**P1/P2** (Single filter):
- `--category X`: Show tasks where `task.category == X` (case-insensitive)
- `--tag Y`: Show tasks where `Y in task.tags` (case-insensitive)

**P3** (Combined filters):
- Multiple filters combine with AND logic
- `--category work --tag urgent`: Show tasks where category is "work" AND tags contain "urgent"

**Validation**:
- No validation needed (any string accepted)
- Non-existent category/tag returns empty list

**Output**:
```
📋 Todo List (Filtered: category=work)

[Rich table with filtered tasks]

Showing 5 of 12 tasks
```

**Empty Results**:
```
📋 Todo List (Filtered: tag=nonexistent)

No tasks found matching your filters.

Try:
  todo list               # View all tasks
  todo list-categories    # View available categories
  todo list-tags          # View available tags
```

**Error Cases**:
- No special errors (empty list is valid result)

---

### 4. `todo list-categories` - List All Categories (NEW)

**Signature**:
```bash
todo list-categories
```

**Arguments**: None

**Examples**:
```bash
todo list-categories
```

**Output**:
```
📂 Categories (3):

  • personal
  • shopping
  • work

Use: todo list --category <name>
```

**Empty State**:
```
📂 Categories

No categories in use yet.

Add a category: todo add "Task title" --category work
```

---

### 5. `todo list-tags` - List All Tags (NEW)

**Signature**:
```bash
todo list-tags
```

**Arguments**: None

**Examples**:
```bash
todo list-tags
```

**Output**:
```
🏷️  Tags (6):

  • bug-fix
  • code-review
  • meeting
  • review
  • urgent
  • work

Use: todo list --tag <name>
```

**Empty State**:
```
🏷️  Tags

No tags in use yet.

Add tags: todo add "Task title" --tags urgent important
```

---

## Argparse Implementation

### Add Command Parser

```python
add_parser = subparsers.add_parser('add', help='Add a new task')
add_parser.add_argument('title', type=str, help='Task title')
add_parser.add_argument('--priority', '-p',
                        choices=['low', 'medium', 'high'],
                        help='Task priority')
add_parser.add_argument('--due', '-d', type=str,
                        help='Due date (YYYY-MM-DD, "today", "tomorrow")')
# NEW ARGUMENTS:
add_parser.add_argument('--category', '-c', type=str,
                        help='Task category (e.g., work, personal)')
add_parser.add_argument('--tags', '-t', nargs='*',
                        help='Task tags (space-separated)')
```

### Update Command Parser

```python
update_parser = subparsers.add_parser('update', help='Update a task')
update_parser.add_argument('id', type=int, help='Task ID')
update_parser.add_argument('--title', type=str, help='New title')
update_parser.add_argument('--priority', '-p',
                          choices=['low', 'medium', 'high'],
                          help='New priority')
update_parser.add_argument('--due', '-d', type=str,
                          help='New due date')
# NEW ARGUMENTS:
update_parser.add_argument('--category', '-c', type=str,
                          help='New category (use "none" to clear)')
update_parser.add_argument('--tags', '-t', nargs='*',
                          help='Replace tags (use "none" to clear)')
```

### List Command Parser

```python
list_parser = subparsers.add_parser('list', help='List tasks')
list_parser.add_argument('--status', '-s',
                        choices=['pending', 'completed', 'all'],
                        default='all',
                        help='Filter by status')
list_parser.add_argument('--priority', '-p',
                        choices=['low', 'medium', 'high'],
                        help='Filter by priority')
# NEW ARGUMENTS:
list_parser.add_argument('--category', '-c', type=str,
                        help='Filter by category')
list_parser.add_argument('--tag', '-t', type=str,
                        help='Filter by tag')
```

### List Categories Parser (NEW)

```python
list_categories_parser = subparsers.add_parser('list-categories',
                                               help='List all categories')
# No arguments needed
```

### List Tags Parser (NEW)

```python
list_tags_parser = subparsers.add_parser('list-tags',
                                         help='List all tags')
# No arguments needed
```

---

## Command Handler Updates

### cmd_add() Implementation

```python
def cmd_add(args: argparse.Namespace) -> int:
    # Extract new arguments
    category = args.category if hasattr(args, 'category') else None
    tags = args.tags if hasattr(args, 'tags') else None

    # Call service with new parameters
    task, error = todo_service.add_task(
        args.title,
        args.priority,
        args.due,
        category=category,
        tags=tags
    )

    if error:
        console_ui.format_error(error)
        return 1

    console_ui.format_task_created(task)
    return 0
```

### cmd_update() Implementation

```python
def cmd_update(args: argparse.Namespace) -> int:
    # Handle "none" special value for category
    category = None
    if hasattr(args, 'category') and args.category:
        if args.category.lower() == "none":
            category = None  # Explicit clear
        else:
            category = args.category

    # Handle "none" special value for tags
    tags = None
    if hasattr(args, 'tags') and args.tags:
        if len(args.tags) == 1 and args.tags[0].lower() == "none":
            tags = []  # Explicit clear
        else:
            tags = args.tags

    # Update task with new parameters
    task, error = todo_service.update_task(
        args.id,
        title=args.title if hasattr(args, 'title') else None,
        priority=args.priority if hasattr(args, 'priority') else None,
        due_date=args.due if hasattr(args, 'due') else None,
        category=category,
        tags=tags
    )

    if error:
        console_ui.format_error(error)
        return 1

    console_ui.format_task_updated(task)
    return 0
```

### cmd_list() Implementation

```python
def cmd_list(args: argparse.Namespace) -> int:
    tasks = todo_service.get_all_tasks()

    # Apply existing filters (status, priority)
    if args.status != 'all':
        tasks = [t for t in tasks if t.status == args.status]
    if hasattr(args, 'priority') and args.priority:
        tasks = [t for t in tasks if t.priority == args.priority]

    # Apply new filters (category, tag)
    if hasattr(args, 'category') and args.category:
        tasks = todo_service.get_tasks_by_category(args.category)

    if hasattr(args, 'tag') and args.tag:
        filtered = todo_service.get_tasks_by_tag(args.tag)
        # If category filter already applied, intersect results
        if hasattr(args, 'category') and args.category:
            task_ids = {t.id for t in tasks}
            tasks = [t for t in filtered if t.id in task_ids]
        else:
            tasks = filtered

    console_ui.format_task_list(tasks)
    return 0
```

### cmd_list_categories() Implementation (NEW)

```python
def cmd_list_categories(args: argparse.Namespace) -> int:
    categories = todo_service.get_all_categories()
    console_ui.format_categories_list(categories)
    return 0
```

### cmd_list_tags() Implementation (NEW)

```python
def cmd_list_tags(args: argparse.Namespace) -> int:
    tags = todo_service.get_all_tags()
    console_ui.format_tags_list(tags)
    return 0
```

---

## Help Text

### Updated `todo --help`

```
usage: todo [-h] {add,update,list,list-categories,list-tags,complete,delete,clear} ...

Simple Todo CLI Application

positional arguments:
  {add,update,list,list-categories,list-tags,complete,delete,clear}
    add                 Add a new task
    update              Update a task
    list                List tasks
    list-categories     List all categories
    list-tags           List all tags
    complete            Mark task as complete
    delete              Delete a task
    clear               Clear all tasks

optional arguments:
  -h, --help            show this help message and exit
```

### `todo add --help`

```
usage: todo add [-h] [--priority {low,medium,high}] [--due DUE]
                [--category CATEGORY] [--tags [TAGS ...]]
                title

positional arguments:
  title                 Task title

optional arguments:
  -h, --help            show this help message and exit
  --priority {low,medium,high}, -p {low,medium,high}
                        Task priority
  --due DUE, -d DUE     Due date (YYYY-MM-DD, "today", "tomorrow")
  --category CATEGORY, -c CATEGORY
                        Task category (e.g., work, personal)
  --tags [TAGS ...], -t [TAGS ...]
                        Task tags (space-separated)
```

### `todo list --help`

```
usage: todo list [-h] [--status {pending,completed,all}]
                 [--priority {low,medium,high}] [--category CATEGORY]
                 [--tag TAG]

optional arguments:
  -h, --help            show this help message and exit
  --status {pending,completed,all}, -s {pending,completed,all}
                        Filter by status (default: all)
  --priority {low,medium,high}, -p {low,medium,high}
                        Filter by priority
  --category CATEGORY, -c CATEGORY
                        Filter by category
  --tag TAG, -t TAG     Filter by tag
```

---

## Edge Cases and Error Handling

### Category/Tag Input Edge Cases

| Input | Handling | Result |
|-------|----------|--------|
| `--category ""` | Convert empty to None | Task has no category |
| `--category "  "` | Strip whitespace → empty → None | Task has no category |
| `--category "Work Project"` | Accept with spaces | Category = "Work Project" |
| `--tags urgent urgent` | Deduplicate | Tags = ["urgent"] |
| `--tags Urgent urgent` | Case-insensitive dedup | Tags = ["Urgent"] (first occurrence kept) |
| `--tags "" urgent` | Filter empty strings | Tags = ["urgent"] |
| `--tags none` in update | Special keyword | Clears all tags |
| No `--category` flag | Default value | category = None |
| No `--tags` flag | Default value | tags = [] |

### Filter Edge Cases

| Input | Handling | Result |
|-------|----------|--------|
| `--category NonExistent` | Valid query, no matches | Empty list displayed |
| `--tag NonExistent` | Valid query, no matches | Empty list displayed |
| `--category work --tag urgent` | AND logic (P3) | Tasks with both conditions |
| `--category ""` | Empty string filter | Shows tasks with category=None (implementation choice) |

---

## Backward Compatibility

- All new arguments are optional (no breaking changes)
- Existing commands work without modification
- Help text updated to show new options
- Old scripts/aliases continue to work

---

## Future Enhancements (Out of Scope)

- `--add-tags` / `--remove-tags`: Append/remove tags without replacing
- `--clear-category`: Explicit flag instead of "none" keyword
- Tag autocomplete with shell completion scripts
- Category/tag validation against predefined lists
- Bulk operations: `todo update-category --from work --to personal`

---

**Status**: Contract complete, ready for implementation
**Next**: See [quickstart.md](../quickstart.md) for usage examples
