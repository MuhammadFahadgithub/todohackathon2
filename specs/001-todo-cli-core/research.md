# Research: Todo CLI Core

**Feature**: 001-todo-cli-core
**Date**: 2026-01-02
**Status**: Complete

## Research Questions

### 1. Python CLI Argument Parsing

**Decision**: Use `argparse` from standard library

**Rationale**:
- Built into Python, no external dependencies
- Supports subcommands for CRUD operations
- Automatic help generation
- Type validation for arguments

**Alternatives Considered**:
| Alternative | Why Rejected |
|-------------|--------------|
| `click` | External dependency, violates Phase 1 constraints |
| `typer` | External dependency, requires type hints runtime |
| `sys.argv` manual | More code, less maintainable, no auto-help |

### 2. In-Memory Data Storage

**Decision**: Use Python `dict` with integer keys for task storage

**Rationale**:
- O(1) lookup by task ID
- Simple to implement
- Easy to iterate for list operations
- No serialization overhead

**Alternatives Considered**:
| Alternative | Why Rejected |
|-------------|--------------|
| List with linear search | O(n) lookup, slower for large lists |
| SQLite in-memory | Overkill for Phase 1, adds complexity |
| dataclasses with slots | Good for Task model, but dict for storage |

### 3. Task Model Design

**Decision**: Use Python `dataclass` with frozen=False for Task model

**Rationale**:
- Clean, readable code
- Automatic `__init__`, `__repr__`
- Type hints for IDE support
- Mutable for updates

**Alternatives Considered**:
| Alternative | Why Rejected |
|-------------|--------------|
| Named tuple | Immutable, harder to update |
| Plain dict | No type safety, harder to maintain |
| Pydantic model | External dependency |

### 4. ID Generation Strategy

**Decision**: Simple incrementing integer counter

**Rationale**:
- Deterministic, predictable
- Easy to test
- Matches spec assumption (IDs start at 1)
- No collision handling needed (single user)

**Alternatives Considered**:
| Alternative | Why Rejected |
|-------------|--------------|
| UUID | Harder for users to type, overkill |
| Timestamp-based | Less user-friendly |
| Hash-based | Unnecessarily complex |

### 5. Output Formatting

**Decision**: Plain text with aligned columns for list output

**Rationale**:
- Works in all terminals
- No color dependency issues
- Easy to parse if needed
- Meets SC-006 (readable, aligned format)

**Alternatives Considered**:
| Alternative | Why Rejected |
|-------------|--------------|
| Rich tables | External dependency |
| JSON output | Less human-readable for primary use |
| ANSI colors | Not universally supported |

### 6. Error Handling Strategy

**Decision**: Return error messages to stderr, exit with non-zero code

**Rationale**:
- Unix convention for CLI tools
- Allows piping stdout without errors
- Clear separation of success/failure

**Pattern**:
```python
# Success
print(f"Task created: {task.title} (ID: {task.id})")
sys.exit(0)

# Error
print(f"Error: Task not found (ID: {task_id})", file=sys.stderr)
sys.exit(1)
```

## Resolved Clarifications

All technical context was clear from spec. No NEEDS CLARIFICATION items.

## Key Decisions Summary

| Topic | Decision | Impact |
|-------|----------|--------|
| CLI Framework | argparse (stdlib) | Zero dependencies |
| Storage | dict with int keys | O(1) operations |
| Task Model | dataclass | Clean, typed |
| IDs | Incrementing int | User-friendly |
| Output | Plain text aligned | Universal compatibility |
| Errors | stderr + exit codes | Unix convention |

## Next Steps

Phase 1 artifacts to generate:
1. `data-model.md` - Task entity definition
2. `contracts/cli-interface.md` - Command interface specification
3. `quickstart.md` - How to run and use the CLI
