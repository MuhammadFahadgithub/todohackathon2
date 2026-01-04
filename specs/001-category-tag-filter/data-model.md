# Data Model: Category and Tag Filtering

**Feature**: 001-category-tag-filter
**Created**: 2026-01-04
**Status**: Design Complete

## Overview

This document describes the data model extensions required to support category and tag filtering in the Todo CLI application. The feature extends the existing `Task` entity with two new fields while maintaining backward compatibility with existing JSON data.

## Entity: Task (Extended)

### Fields

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| id | int | Yes | Auto-increment | Unique task identifier |
| title | str | Yes | - | Task description |
| status | str | Yes | "pending" | Task status: "pending" or "completed" |
| priority | Optional[str] | No | None | Task priority: "low", "medium", "high" |
| due_date | Optional[datetime] | No | None | Task due date |
| created_at | datetime | Yes | now() | Timestamp when task was created |
| completed_at | Optional[datetime] | No | None | Timestamp when task was completed |
| **category** | **Optional[str]** | **No** | **None** | **Task category (single string)** |
| **tags** | **List[str]** | **No** | **[]** | **Task tags (list of strings)** |

### New Fields Detail

#### category: Optional[str]

- **Purpose**: Classify tasks into mutually exclusive groups (e.g., "work", "personal", "shopping")
- **Constraints**:
  - Optional field (can be None)
  - Single string value per task
  - Case-insensitive matching ("work" == "Work" == "WORK")
  - Whitespace trimmed on storage
  - Empty strings treated as None
  - No maximum length enforced (reasonable user behavior assumed)
- **Examples**: "work", "personal", "shopping", "health", "finance"

#### tags: List[str]

- **Purpose**: Apply multiple cross-cutting labels to tasks (e.g., "urgent", "bug-fix", "meeting")
- **Constraints**:
  - List of strings (can be empty list)
  - Multiple values per task allowed
  - Case-insensitive matching ("urgent" == "Urgent" == "URGENT")
  - Duplicates automatically removed (case-insensitive)
  - Whitespace trimmed for each tag
  - No maximum tag count enforced
  - Tag order not guaranteed to be preserved
- **Examples**: ["urgent", "bug-fix"], ["meeting", "important"], ["review", "code", "urgent"]

### Python Dataclass Definition

```python
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List

@dataclass
class Task:
    id: int
    title: str
    status: str = "pending"
    priority: Optional[str] = None
    due_date: Optional[datetime] = None
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    category: Optional[str] = None  # NEW FIELD
    tags: List[str] = field(default_factory=list)  # NEW FIELD
```

## Validation Rules

### Category Validation

1. **Empty string handling**: Convert empty strings to None
2. **Whitespace handling**: Strip leading/trailing whitespace
3. **Case normalization**: Store as provided, match case-insensitively
4. **Special values**: "none" (lowercase) treated as explicit clear request in CLI

**Validation pseudocode**:
```python
def validate_category(category: Optional[str]) -> Optional[str]:
    if category is None:
        return None

    category = category.strip()

    if category == "":
        return None

    return category
```

### Tags Validation

1. **Duplicate removal**: Remove duplicates case-insensitively
2. **Whitespace handling**: Strip each tag
3. **Empty tag removal**: Filter out empty strings
4. **Case normalization**: Store as provided, match case-insensitively
5. **Special values**: "none" (lowercase) as single tag treated as clear request in CLI

**Validation pseudocode**:
```python
def validate_tags(tags: Optional[List[str]]) -> List[str]:
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
```

## State Transitions

Category and tags are mutable attributes with no state machine. They can be:
- Set at task creation
- Updated at any time
- Cleared at any time
- Remain unchanged when task status changes (pending → completed)

## Persistence Format (JSON)

### New Task Format

```json
{
  "id": 5,
  "title": "Review pull request",
  "status": "pending",
  "priority": "high",
  "due_date": "2026-01-10T00:00:00",
  "created_at": "2026-01-04T10:30:00",
  "completed_at": null,
  "category": "work",
  "tags": ["urgent", "code-review", "bug-fix"]
}
```

### Backward Compatibility

Old tasks without category/tags fields load correctly:

```json
{
  "id": 1,
  "title": "Old task",
  "status": "pending",
  "priority": "medium",
  "due_date": null,
  "created_at": "2026-01-01T09:00:00",
  "completed_at": null
}
```

**Loading behavior**: Uses `.get("category")` and `.get("tags", [])` to provide defaults (None and [] respectively).

## Indexing and Filtering

### Category Index

No explicit index maintained. Filtering is O(n) linear scan:

```python
def get_tasks_by_category(category: str) -> List[Task]:
    return [t for t in tasks
            if t.category and t.category.lower() == category.lower()]
```

**Performance**: Acceptable for CLI tool with expected task count < 1000.

### Tag Index

No explicit index maintained. Filtering is O(n*m) where m is average tag count:

```python
def get_tasks_by_tag(tag: str) -> List[Task]:
    return [t for t in tasks
            if tag.lower() in [t_tag.lower() for t_tag in t.tags]]
```

**Performance**: Acceptable given typical tag count (2-5 per task).

## Entity Relationships

```
Task (1) ----< (0..1) Category (string, not an entity)
Task (1) ----< (0..*) Tag (string, not an entity)
```

**Note**: Categories and tags are simple string attributes, not separate entities with their own lifecycle. They exist only as attributes of tasks.

## Query Operations

### Supported Queries

1. **Get tasks by category**: Return all tasks matching a category (case-insensitive)
2. **Get tasks by tag**: Return all tasks containing a tag (case-insensitive)
3. **Get all unique categories**: Return sorted list of all categories in use
4. **Get all unique tags**: Return sorted list of all tags in use
5. **Combined filter** (P3): Return tasks matching both category AND tag

### Query Examples

```python
# Get all work tasks
work_tasks = service.get_tasks_by_category("work")

# Get all urgent tasks
urgent_tasks = service.get_tasks_by_tag("urgent")

# List all categories
categories = service.get_all_categories()
# Returns: ["personal", "shopping", "work"]

# List all tags
tags = service.get_all_tags()
# Returns: ["bug-fix", "code-review", "meeting", "urgent"]
```

## Migration Strategy

**No migration required** - backward compatible:

1. Existing tasks load with `category=None` and `tags=[]`
2. Updated tasks save with new fields included
3. Old CLI versions ignore new fields (forward compatible)
4. New CLI versions handle missing fields gracefully (backward compatible)

## Design Rationale

### Why not separate Category/Tag entities?

- **Simplicity**: Categories and tags are just labels, not complex entities
- **Performance**: No joins or lookups needed for in-memory CLI tool
- **Storage**: JSON naturally handles string lists without schema complexity
- **Scope**: No requirement for category/tag metadata (descriptions, colors, etc.)

### Why case-insensitive matching?

- **User expectations**: Most users expect "Work" and "work" to be the same
- **Error prevention**: Reduces accidental duplication due to typos
- **Consistency**: Aligns with common CLI tool behavior

### Why list for tags instead of set?

- **JSON compatibility**: Lists serialize naturally to JSON arrays
- **Order preservation**: Although order not guaranteed, lists support it if needed later
- **Simplicity**: dataclasses work better with lists than sets

## Future Considerations (Out of Scope)

- **Category hierarchies**: e.g., "work/projects/client-a"
- **Tag metadata**: colors, descriptions, creation dates
- **Tag relationships**: parent/child tags, synonyms
- **Analytics**: most-used tags, category distribution
- **Bulk operations**: rename category across all tasks, merge tags

---

**Status**: Design complete, ready for implementation
**Next**: See [contracts/](./contracts/) for CLI API contracts
