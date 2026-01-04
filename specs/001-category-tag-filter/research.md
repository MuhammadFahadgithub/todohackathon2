# Research: Category and Tag Filtering

**Feature**: 001-category-tag-filter
**Date**: 2026-01-04
**Status**: Complete

## Research Questions

### R1: Case-Insensitive String Matching in Python

**Question**: How should we implement case-insensitive matching for categories and tags?

**Options Evaluated**:
1. **`.lower()` comparison** - Convert both strings to lowercase before comparing
2. **Regular expressions** - Use `re.IGNORECASE` flag
3. **Third-party library** - Use library like `python-string-utils`

**Decision**: Use `.lower()` comparison

**Rationale**:
- Simple and readable
- No additional dependencies
- Standard Python idiom
- Performs well for small datasets (our use case)
- Works consistently across all string operations

**Implementation**:
```python
# Category matching
if task.category and task.category.lower() == filter_category.lower():
    # match

# Tag matching
if any(tag.lower() == filter_tag.lower() for tag in task.tags):
    # match
```

---

### R2: CLI Argument Parsing for Lists

**Question**: How should users specify multiple tags via CLI?

**Options Evaluated**:
1. **Space-separated with `nargs='*'`** - `--tags urgent bug-fix meeting`
2. **Comma-separated** - `--tags urgent,bug-fix,meeting`
3. **Multiple flags** - `--tag urgent --tag bug-fix --tag meeting`

**Decision**: Space-separated with `nargs='*'`

**Rationale**:
- Most natural for CLI users
- Standard argparse pattern
- No additional parsing required
- Consistent with how most CLI tools handle lists
- Shell completion works naturally

**Implementation**:
```python
add_parser.add_argument('--tags', '-t', nargs='*',
                       help='Task tags (space-separated)')
# Usage: todo add "Title" --tags urgent bug-fix
```

**Trade-offs**:
- Tags with spaces require quoting: `--tags "high priority" urgent`
- Acceptable given tags should be short keywords

---

### R3: Rich Table Display for Lists

**Question**: How should we display multiple tags in a Rich table cell?

**Options Evaluated**:
1. **Comma-separated string** - `"urgent, bug-fix, meeting"`
2. **Badges with styling** - Colored pill-shaped badges
3. **Vertical list** - One tag per line (multi-row cell)
4. **Truncated with tooltip** - Show first N tags, hover for more

**Decision**: Comma-separated string with truncation

**Rationale**:
- Simple to implement
- Works with existing Rich Table
- Readable at a glance
- No complex styling needed
- Truncation prevents table width overflow

**Implementation**:
```python
# In console.py format_task_list()
tags_display = ", ".join(task.tags[:5])  # Limit to 5
if len(task.tags) > 5:
    tags_display += ", ..."
```

**Alternative for Future**: Consider Rich's `[tag]` markup for styled badges if time permits.

---

### R4: Duplicate Tag Prevention

**Question**: How should we handle duplicate tags when user adds them?

**Options Evaluated**:
1. **Silent deduplication** - Remove duplicates automatically
2. **Error message** - Reject the operation with error
3. **Warning with deduplication** - Show warning but proceed

**Decision**: Silent deduplication with set operations

**Rationale**:
- User-friendly (no errors for innocent mistakes)
- Simple implementation
- Order preservation not critical for tags
- Aligns with user expectations (tags are unique identifiers)

**Implementation**:
```python
# When adding tags
if tags:
    # Remove duplicates while preserving some order
    tags = list(dict.fromkeys(t.lower() for t in tags))
```

**Note**: Case-insensitive deduplication - "Urgent" and "urgent" are same tag.

---

## Dependencies Analysis

### Existing Dependencies

**Rich 14.2.0** - Terminal UI library
- Already in use for table display
- Supports all our needs (tables, colors, text styling)
- **No changes required**

**python-dateutil** - Date parsing library
- Already in use for due date parsing
- Not used for category/tags feature
- **No changes required**

**Standard Library**:
- `dataclasses` - For Task model
- `json` - For persistence
- `argparse` - For CLI parsing
- `typing` - For type hints
- **All sufficient for our needs**

### New Dependencies

**None required** - Feature uses existing infrastructure.

---

## Integration Points

### IP1: Task Model (src/models/task.py)

**Status**: ✅ Already implemented

**Changes Made**:
```python
from typing import Optional, List

@dataclass
class Task:
    # ... existing fields ...
    category: Optional[str] = None
    tags: List[str] = field(default_factory=list)
```

**Impact**: All existing Task instances still work (optional fields with defaults).

---

### IP2: Persistence (src/services/persistence.py)

**Status**: ✅ Already implemented

**Changes Made**:
- JSON serialization includes `category` and `tags` fields
- JSON deserialization uses `.get()` with defaults for backward compatibility

**Backward Compatibility Test**:
```json
// Old format (before feature)
{"id": 1, "title": "Task", "status": "pending", ...}

// New format (after feature)
{"id": 1, "title": "Task", "status": "pending", "category": "work", "tags": ["urgent"], ...}
```
✅ Old tasks load with `category=None`, `tags=[]`

---

### IP3: Service Layer (src/services/todo_service.py)

**Status**: ⏳ Partially implemented

**Completed**:
- ✅ `get_tasks_by_category(category: str)` - Filter by category
- ✅ `get_tasks_by_tag(tag: str)` - Filter by tag
- ✅ `get_all_categories()` - List unique categories
- ✅ `get_all_tags()` - List unique tags

**Pending**:
- ⏳ Update `add_task()` signature to accept `category` and `tags` parameters
- ⏳ Update `update_task()` to handle category/tags changes
- ⏳ Add duplicate tag prevention logic

---

### IP4: CLI Interface (src/main.py)

**Status**: ⏳ Not started

**Required Changes**:
1. Add `--category` and `--tags` to `add` command parser
2. Add `--category` and `--tags` to `update` command parser
3. Add `--category` filter to `list` command parser
4. Add `--tag` filter to `list` command parser
5. Update `cmd_add()` to pass category/tags to service
6. Update `cmd_update()` to pass category/tags to service
7. Update `cmd_list()` to apply category/tag filters

---

### IP5: Rich UI (src/ui/console.py)

**Status**: ⏳ Not started

**Required Changes**:
1. Add "Category" column to task list table
2. Add "Tags" column to task list table
3. Update `format_task_created()` to show category/tags
4. Update `format_task_updated()` to show category/tags changes
5. Format tags as comma-separated string
6. Truncate long tag lists with "..."

---

## Best Practices Applied

### CLI Design Principles

1. **Consistency**: Use same flag names across commands (`--category`, `--tags`)
2. **Discoverability**: Include examples in help text
3. **Error Messages**: Clear, actionable error messages for invalid input
4. **Backward Compatibility**: Optional flags don't break existing commands

### Code Quality

1. **Type Hints**: All functions have proper type annotations
2. **Case-Insensitive**: User expectations met (work = Work = WORK)
3. **Data Validation**: Strip whitespace, handle empty strings
4. **Performance**: O(n) filtering is acceptable for in-memory CLI tool

### User Experience

1. **Helpful Defaults**: Empty category/tags list is valid state
2. **Easy Correction**: User can update category/tags after creation
3. **Visual Clarity**: Tags comma-separated, not cluttered
4. **Intuitive Filtering**: Single filter at a time (P1/P2), combined later (P3)

---

## Open Questions

**None** - All research complete, ready for implementation.

---

## Next Steps

1. Run `/sp.tasks` to generate detailed task breakdown
2. Implement P1 tasks (CLI + basic display)
3. Test with manual checklist
4. Implement P2 tasks (enhanced display)
5. Optional: Implement P3 tasks (advanced features)
