# Implementation Plan: Todo CLI Core

**Branch**: `001-todo-cli-core` | **Date**: 2026-01-02 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-todo-cli-core/spec.md`

## Summary

Implement a command-line todo application with full CRUD operations (add, list, update, delete, complete) for task management. The application uses in-memory storage, supports task priorities, and provides clear user feedback for all operations. This is a single-user, local CLI tool with no persistence between sessions (Phase 1 scope).

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: None (standard library only for Phase 1)
**Storage**: In-memory (Python list/dict)
**Testing**: pytest
**Target Platform**: Cross-platform CLI (Windows, macOS, Linux)
**Project Type**: Single project
**Performance Goals**: All operations complete in <2 seconds (per SC-001)
**Constraints**: No external dependencies, in-memory only, single-user
**Scale/Scope**: Single user, up to 1000+ tasks (per edge case)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Evidence |
|-----------|--------|----------|
| I. Spec Before Code | PASS | `/sp.specify` completed, spec.md exists |
| II. Small & Verifiable Changes | PASS | 5 user stories, each independently testable |
| III. Single Source of Truth | PASS | All requirements in spec.md, no assumptions |
| IV. Explicit Decisions | PASS | Tech stack documented below |

**Constitution Compliance**: All gates pass. Ready for Phase 0.

## Project Structure

### Documentation (this feature)

```text
specs/001-todo-cli-core/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output (CLI interface contracts)
└── tasks.md             # Phase 2 output (/sp.tasks command)
```

### Source Code (repository root)

```text
src/
├── __init__.py
├── main.py              # CLI entry point and argument parsing
├── models/
│   ├── __init__.py
│   └── task.py          # Task dataclass/model
├── services/
│   ├── __init__.py
│   └── todo_service.py  # Business logic for CRUD operations
└── ui/
    ├── __init__.py
    └── console.py       # Output formatting and display

tests/
├── __init__.py
├── unit/
│   ├── __init__.py
│   ├── test_task.py
│   └── test_todo_service.py
└── integration/
    ├── __init__.py
    └── test_cli.py
```

**Structure Decision**: Single project structure selected. CLI application with clear separation:
- `models/` - Data structures (Task)
- `services/` - Business logic (TodoService)
- `ui/` - Presentation layer (Console output)
- `main.py` - Entry point with argparse

## Complexity Tracking

> No violations detected. Structure follows minimal viable approach.

| Aspect | Decision | Rationale |
|--------|----------|-----------|
| No ORM | Direct dict storage | In-memory only, no persistence needed |
| No framework | Standard library argparse | Minimal dependencies per constitution |
| No abstract base classes | Concrete implementations | YAGNI - single implementation needed |
