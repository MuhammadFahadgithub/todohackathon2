# Data Model: Todo CLI Core

**Feature**: 001-todo-cli-core
**Date**: 2026-01-02

## Entities

### Task

Represents a single todo item in the system.

| Attribute | Type | Required | Default | Constraints |
|-----------|------|----------|---------|-------------|
| `id` | integer | Yes | Auto-generated | Unique, positive, incrementing from 1 |
| `title` | string | Yes | - | Non-empty, max 500 characters |
| `status` | enum | Yes | "pending" | One of: "pending", "completed" |
| `priority` | enum | Yes | "medium" | One of: "low", "medium", "high" |
| `created_at` | datetime | Yes | Current time | ISO 8601 format |

### Enumerations

#### TaskStatus

| Value | Description |
|-------|-------------|
| `pending` | Task is not yet completed |
| `completed` | Task has been marked as done |

#### TaskPriority

| Value | Description |
|-------|-------------|
| `low` | Low priority task |
| `medium` | Normal priority (default) |
| `high` | High priority task |

## State Transitions

### Task Lifecycle

```text
[NEW] ---(create)---> [PENDING] ---(complete)---> [COMPLETED]
                           |                            |
                           +----(delete)---->[DELETED]<-+
                           |                            |
                           +----(update)--->[PENDING]---+
```

| Transition | From State | To State | Trigger |
|------------|------------|----------|---------|
| Create | (none) | pending | `add` command |
| Complete | pending | completed | `complete` command |
| Complete | completed | completed | `complete` command (idempotent) |
| Update | any | (same) | `update` command |
| Delete | any | (removed) | `delete` command |

## Validation Rules

### Task Creation (FR-001, FR-009)

1. Title MUST be provided
2. Title MUST NOT be empty (whitespace-only rejected)
3. Title MUST NOT exceed 500 characters
4. Priority MUST be one of: low, medium, high
5. If priority not specified, default to "medium"

### Task Update (FR-007, FR-009)

1. Task with given ID MUST exist
2. If title provided, MUST NOT be empty
3. If title provided, MUST NOT exceed 500 characters
4. If priority provided, MUST be one of: low, medium, high

### Task Completion (FR-006)

1. Task with given ID MUST exist
2. Already-completed tasks remain completed (no error)

### Task Deletion (FR-008)

1. Task with given ID MUST exist

## Storage Schema

### In-Memory Structure

```python
# Task storage: dict[int, Task]
tasks: dict[int, Task] = {}

# ID counter: tracks next available ID
next_id: int = 1
```

### Example State

```python
{
    1: Task(id=1, title="Buy groceries", status="pending", priority="medium", created_at="2026-01-02T10:00:00"),
    2: Task(id=2, title="Call mom", status="completed", priority="high", created_at="2026-01-02T10:05:00"),
    3: Task(id=3, title="Finish report", status="pending", priority="high", created_at="2026-01-02T10:10:00"),
}
```

## Relationships

No relationships in Phase 1. Task is a standalone entity.

Future considerations (out of scope):
- Task → Category (many-to-one)
- Task → Tags (many-to-many)
- Task → Reminder (one-to-many)
