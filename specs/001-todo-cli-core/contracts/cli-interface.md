# CLI Interface Contract: Todo CLI Core

**Feature**: 001-todo-cli-core
**Date**: 2026-01-02

## Overview

This document defines the command-line interface contract for the Todo CLI application. All commands follow Unix conventions with subcommand pattern.

## Base Command

```bash
python -m src.main <command> [options]
```

Or after installation:

```bash
todo <command> [options]
```

## Commands

### add - Create a new task (FR-001, FR-002, FR-003)

**Usage**:
```bash
todo add <title> [--priority <level>]
```

**Arguments**:

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `title` | string | Yes | Task title (max 500 chars) |

**Options**:

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--priority`, `-p` | enum | medium | Priority: low, medium, high |

**Success Output** (stdout):
```
Created task: <title> (ID: <id>)
Priority: <priority>
```

**Error Output** (stderr):
```
Error: Title cannot be empty
Error: Title exceeds 500 characters
Error: Invalid priority '<value>'. Must be: low, medium, high
```

**Exit Codes**:
- `0`: Task created successfully
- `1`: Validation error

---

### list - Display tasks (FR-004, FR-005)

**Usage**:
```bash
todo list [--status <filter>]
```

**Options**:

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--status`, `-s` | enum | all | Filter: all, pending, completed |

**Success Output** (stdout):
```
ID    Status      Priority   Title
----  ----------  ---------  --------------------------------------------------
1     pending     medium     Buy groceries
2     completed   high       Call mom
3     pending     high       Finish report

Total: 3 tasks (2 pending, 1 completed)
```

**Empty List Output** (stdout):
```
No tasks found.

Tip: Add a task with 'todo add "Your task title"'
```

**Exit Codes**:
- `0`: Always (list operation cannot fail)

---

### complete - Mark task as completed (FR-006)

**Usage**:
```bash
todo complete <id>
```

**Arguments**:

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `id` | integer | Yes | Task ID to complete |

**Success Output** (stdout):
```
Completed task: <title> (ID: <id>)
```

**Already Completed Output** (stdout):
```
Task already completed: <title> (ID: <id>)
```

**Error Output** (stderr):
```
Error: Task not found (ID: <id>)
Error: Invalid ID '<value>'. Must be a number.
```

**Exit Codes**:
- `0`: Task completed or already completed
- `1`: Task not found or invalid ID

---

### update - Modify task details (FR-007)

**Usage**:
```bash
todo update <id> [--title <new_title>] [--priority <level>]
```

**Arguments**:

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `id` | integer | Yes | Task ID to update |

**Options**:

| Option | Type | Required | Description |
|--------|------|----------|-------------|
| `--title`, `-t` | string | No | New title (max 500 chars) |
| `--priority`, `-p` | enum | No | New priority: low, medium, high |

**Note**: At least one of `--title` or `--priority` must be provided.

**Success Output** (stdout):
```
Updated task (ID: <id>):
  Title: <old_title> → <new_title>
  Priority: <old_priority> → <new_priority>
```

**Error Output** (stderr):
```
Error: Task not found (ID: <id>)
Error: Invalid ID '<value>'. Must be a number.
Error: Title cannot be empty
Error: Title exceeds 500 characters
Error: No changes specified. Use --title or --priority.
```

**Exit Codes**:
- `0`: Task updated successfully
- `1`: Validation error or task not found

---

### delete - Remove a task (FR-008)

**Usage**:
```bash
todo delete <id>
```

**Arguments**:

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `id` | integer | Yes | Task ID to delete |

**Success Output** (stdout):
```
Deleted task: <title> (ID: <id>)
```

**Error Output** (stderr):
```
Error: Task not found (ID: <id>)
Error: Invalid ID '<value>'. Must be a number.
```

**Exit Codes**:
- `0`: Task deleted successfully
- `1`: Task not found or invalid ID

---

## Global Options

| Option | Description |
|--------|-------------|
| `--help`, `-h` | Show help for command |
| `--version`, `-v` | Show version number |

## Exit Code Summary

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | User error (validation, not found) |
| 2 | System error (unexpected) |

## Output Formatting

### Column Widths (list command)

| Column | Width | Alignment |
|--------|-------|-----------|
| ID | 4 | Right |
| Status | 10 | Left |
| Priority | 9 | Left |
| Title | 50 | Left (truncated with ... if longer) |

### Error Message Format

All errors follow the pattern:
```
Error: <description>
```

Suggestions follow errors when applicable:
```
Error: <description>

Tip: <suggestion>
```
