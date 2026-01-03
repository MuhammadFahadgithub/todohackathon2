# Tasks: Todo CLI Core

**Input**: Design documents from `/specs/001-todo-cli-core/`
**Prerequisites**: plan.md (required), spec.md (required), data-model.md, contracts/cli-interface.md, quickstart.md

**Tests**: Tests are NOT explicitly requested in the spec. Test tasks are omitted per task generation rules.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story?] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Paths follow plan.md structure

---

## Phase 1: Setup

**Purpose**: Project initialization and basic structure

- [x] T001 Create project directory structure per plan.md (src/, src/models/, src/services/, src/ui/)
- [x] T002 [P] Create src/__init__.py with package initialization
- [x] T003 [P] Create src/models/__init__.py with package initialization
- [x] T004 [P] Create src/services/__init__.py with package initialization
- [x] T005 [P] Create src/ui/__init__.py with package initialization

**Checkpoint**: Project structure ready for foundational code

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**CRITICAL**: No user story work can begin until this phase is complete

- [x] T006 Create TaskStatus enum (pending, completed) in src/models/task.py
- [x] T007 Create TaskPriority enum (low, medium, high) in src/models/task.py
- [x] T008 Create Task dataclass with id, title, status, priority, created_at in src/models/task.py
- [x] T009 Create TodoService class with tasks dict and next_id counter in src/services/todo_service.py
- [x] T010 [P] Create ConsoleUI class with output formatting methods in src/ui/console.py
- [x] T011 Create CLI entry point with argparse subcommands skeleton in src/main.py

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Add a New Task (Priority: P1)

**Goal**: Users can add tasks with title and optional priority

**Independent Test**: Run `python -m src.main add "Buy groceries"` and verify task is created with ID 1

**Functional Requirements**: FR-001, FR-002, FR-003, FR-009, FR-010, FR-011, FR-012

### Implementation for User Story 1

- [x] T012 [US1] Implement add_task(title, priority) method in src/services/todo_service.py
- [x] T013 [US1] Add title validation (non-empty, max 500 chars) to add_task in src/services/todo_service.py
- [x] T014 [US1] Add priority validation and default to add_task in src/services/todo_service.py
- [x] T015 [US1] Implement format_task_created() output method in src/ui/console.py
- [x] T016 [US1] Implement add subcommand with --priority option in src/main.py
- [x] T017 [US1] Wire add subcommand to TodoService.add_task() in src/main.py

**Checkpoint**: User Story 1 complete - users can add tasks

---

## Phase 4: User Story 2 - List All Tasks (Priority: P1)

**Goal**: Users can view all tasks with filtering by status

**Independent Test**: Add tasks, run `python -m src.main list` and verify all tasks display correctly

**Functional Requirements**: FR-004, FR-005, FR-010, FR-011

### Implementation for User Story 2

- [x] T018 [US2] Implement get_all_tasks() method in src/services/todo_service.py
- [x] T019 [US2] Implement get_tasks_by_status(status) method in src/services/todo_service.py
- [x] T020 [US2] Implement format_task_list(tasks) with aligned columns in src/ui/console.py
- [x] T021 [US2] Implement format_empty_list() with tip message in src/ui/console.py
- [x] T022 [US2] Implement list subcommand with --status filter in src/main.py
- [x] T023 [US2] Wire list subcommand to TodoService methods in src/main.py

**Checkpoint**: User Stories 1 & 2 complete - MVP functional (add + list)

---

## Phase 5: User Story 3 - Complete a Task (Priority: P2)

**Goal**: Users can mark tasks as completed

**Independent Test**: Add task, run `python -m src.main complete 1`, verify status changes to completed

**Functional Requirements**: FR-006, FR-010, FR-011

### Implementation for User Story 3

- [x] T024 [US3] Implement get_task_by_id(task_id) method in src/services/todo_service.py
- [x] T025 [US3] Implement complete_task(task_id) method in src/services/todo_service.py
- [x] T026 [US3] Handle already-completed tasks (return informational message) in src/services/todo_service.py
- [x] T027 [US3] Implement format_task_completed() output method in src/ui/console.py
- [x] T028 [US3] Implement format_task_already_completed() output method in src/ui/console.py
- [x] T029 [US3] Implement complete subcommand in src/main.py
- [x] T030 [US3] Add task ID validation (must be integer) to complete subcommand in src/main.py

**Checkpoint**: User Story 3 complete - users can complete tasks

---

## Phase 6: User Story 4 - Update a Task (Priority: P2)

**Goal**: Users can update task title and/or priority

**Independent Test**: Add task, run `python -m src.main update 1 --title "New title"`, verify change

**Functional Requirements**: FR-007, FR-009, FR-010, FR-011

### Implementation for User Story 4

- [x] T031 [US4] Implement update_task(task_id, title, priority) method in src/services/todo_service.py
- [x] T032 [US4] Add validation for at least one change required in update_task in src/services/todo_service.py
- [x] T033 [US4] Implement format_task_updated() showing old/new values in src/ui/console.py
- [x] T034 [US4] Implement update subcommand with --title and --priority options in src/main.py
- [x] T035 [US4] Add task ID validation to update subcommand in src/main.py

**Checkpoint**: User Story 4 complete - users can update tasks

---

## Phase 7: User Story 5 - Delete a Task (Priority: P3)

**Goal**: Users can delete tasks from the list

**Independent Test**: Add task, run `python -m src.main delete 1`, verify task removed from list

**Functional Requirements**: FR-008, FR-010, FR-011

### Implementation for User Story 5

- [x] T036 [US5] Implement delete_task(task_id) method in src/services/todo_service.py
- [x] T037 [US5] Implement format_task_deleted() output method in src/ui/console.py
- [x] T038 [US5] Implement delete subcommand in src/main.py
- [x] T039 [US5] Add task ID validation to delete subcommand in src/main.py

**Checkpoint**: All user stories complete - full CRUD functionality

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Error handling, edge cases, and final touches

- [x] T040 [P] Implement format_error() for stderr output in src/ui/console.py
- [x] T041 [P] Implement format_task_not_found() error message in src/ui/console.py
- [x] T042 [P] Implement format_invalid_id() error message in src/ui/console.py
- [x] T043 Add --help and --version global options in src/main.py
- [x] T044 Verify all exit codes match contract (0=success, 1=user error) in src/main.py
- [x] T045 Test edge case: task title at 500 character limit
- [x] T046 Test edge case: special characters in title (quotes, unicode)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-7)**: All depend on Foundational phase completion
  - US1 and US2 can run in parallel (both P1)
  - US3 depends on US1 (needs tasks to complete)
  - US4 depends on US1 (needs tasks to update)
  - US5 depends on US1 (needs tasks to delete)
- **Polish (Phase 8)**: Depends on all user stories being complete

### User Story Dependencies

| Story | Depends On | Can Start After |
|-------|------------|-----------------|
| US1 (Add) | Foundational | Phase 2 complete |
| US2 (List) | Foundational | Phase 2 complete |
| US3 (Complete) | US1 | Phase 3 complete |
| US4 (Update) | US1 | Phase 3 complete |
| US5 (Delete) | US1 | Phase 3 complete |

### Within Each User Story

- Service methods before CLI integration
- UI formatting can be parallel with service methods
- CLI wiring depends on both service and UI

### Parallel Opportunities

- T002-T005: All package __init__.py files
- T010: ConsoleUI can be built parallel to TodoService
- US1 + US2: Both P1 stories can be developed in parallel
- US3, US4, US5: Can be developed in parallel after US1 complete
- T040-T042: All error formatting methods

---

## Parallel Example: Phase 2 Foundation

```bash
# Launch all parallelizable tasks together:
Task T002: "Create src/__init__.py"
Task T003: "Create src/models/__init__.py"
Task T004: "Create src/services/__init__.py"
Task T005: "Create src/ui/__init__.py"
Task T010: "Create ConsoleUI class in src/ui/console.py"
```

## Parallel Example: User Story 1

```bash
# Service and UI can be parallel:
Task T012: "Implement add_task method in src/services/todo_service.py"
Task T015: "Implement format_task_created in src/ui/console.py"

# Then CLI integration:
Task T016: "Implement add subcommand in src/main.py"
Task T017: "Wire add subcommand to TodoService"
```

---

## Implementation Strategy

### MVP First (User Stories 1 & 2 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (Add)
4. Complete Phase 4: User Story 2 (List)
5. **STOP and VALIDATE**: Test add and list independently
6. Deploy/demo if ready - this is a functional MVP!

### Incremental Delivery

1. Setup + Foundational → Foundation ready
2. Add User Story 1 (Add) → Test → Partial value
3. Add User Story 2 (List) → Test → **MVP complete!**
4. Add User Story 3 (Complete) → Test → Enhanced value
5. Add User Story 4 (Update) → Test → Full editing
6. Add User Story 5 (Delete) → Test → **Feature complete!**
7. Polish phase → Production ready

---

## Task Summary

| Phase | Task Count | Parallel Tasks |
|-------|------------|----------------|
| Setup | 5 | 4 |
| Foundational | 6 | 1 |
| US1 (Add) | 6 | 0 |
| US2 (List) | 6 | 0 |
| US3 (Complete) | 7 | 0 |
| US4 (Update) | 5 | 0 |
| US5 (Delete) | 4 | 0 |
| Polish | 7 | 3 |
| **Total** | **46** | **8** |

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story is independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- MVP = Phase 1-4 complete (Setup + Foundational + Add + List)
