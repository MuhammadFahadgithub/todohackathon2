---
description: "Task breakdown for category and tag filtering feature"
---

# Tasks: Category and Tag Filtering

**Input**: Design documents from `/specs/001-category-tag-filter/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/, quickstart.md

**Tests**: Tests are OPTIONAL for this hackathon project. Manual testing with quickstart.md validation will be used instead of automated tests.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

Single project structure:
- `src/` - Source code root
- `src/models/` - Data models
- `src/services/` - Business logic
- `src/ui/` - Console UI
- `src/main.py` - CLI entry point

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and verification of existing structure

**Current State**: Model and persistence already extended with category/tags fields. This phase verifies the foundation is ready.

- [X] T001 Verify Task model has category and tags fields in src/models/task.py
- [X] T002 Verify persistence layer serializes category/tags in src/services/persistence.py
- [X] T003 Verify service layer has filter methods in src/services/todo_service.py

**Checkpoint**: Foundation verified - user story implementation can begin

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Service layer signature updates that all user stories depend on

**⚠️ CRITICAL**: These updates MUST be complete before CLI integration can proceed

- [X] T004 Update add_task() signature to accept category and tags parameters in src/services/todo_service.py
- [X] T005 Update update_task() signature to accept category and tags parameters in src/services/todo_service.py
- [X] T006 Implement category validation (strip whitespace, convert empty to None) in src/services/todo_service.py
- [X] T007 Implement tags validation (deduplicate, strip whitespace, remove empty) in src/services/todo_service.py

**Checkpoint**: Service layer ready - CLI and UI integration can now proceed in parallel

---

## Phase 3: User Story 1 - Organize Tasks by Category (Priority: P1) 🎯 MVP

**Goal**: Users can assign a single category to tasks and filter tasks by category

**Independent Test**:
1. Add task with `--category work`
2. Add task with `--category personal`
3. Filter with `todo list --category work`
4. Verify only work tasks shown
5. Verify category displayed in task list

**Acceptance Scenarios from Spec**:
- Given no tasks exist, When user creates task with category "work", Then task created with category
- Given 5 tasks with mixed categories, When user filters by "personal", Then only personal tasks displayed
- Given task with category "work", When user updates to "personal", Then category changed
- Given multiple tasks, When user lists categories, Then all distinct categories displayed

### Implementation for User Story 1

- [X] T008 [P] [US1] Add --category argument to 'add' command parser in src/main.py
- [X] T009 [P] [US1] Add --category argument to 'update' command parser in src/main.py
- [X] T010 [P] [US1] Add --category filter argument to 'list' command parser in src/main.py
- [X] T011 [US1] Update cmd_add() to pass category parameter to add_task() in src/main.py
- [X] T012 [US1] Update cmd_update() to handle category parameter (including "none" for clearing) in src/main.py
- [X] T013 [US1] Update cmd_list() to apply category filter using get_tasks_by_category() in src/main.py
- [X] T014 [P] [US1] Add "Category" column to task list table in src/ui/console.py
- [X] T015 [P] [US1] Display category in format_task_created() output in src/ui/console.py
- [X] T016 [P] [US1] Display category changes in format_task_updated() output in src/ui/console.py
- [X] T017 [US1] Add list-categories command parser in src/main.py
- [X] T018 [US1] Implement cmd_list_categories() handler in src/main.py
- [X] T019 [US1] Implement format_categories_list() in src/ui/console.py

**Manual Testing Checklist for US1**:
- [ ] Create task with category: `todo add "Test task" --category work`
- [ ] Verify category shown in output
- [ ] List by category: `todo list --category work`
- [ ] Verify filtering works (case-insensitive)
- [ ] Update category: `todo update 1 --category personal`
- [ ] Clear category: `todo update 1 --category none`
- [ ] List all categories: `todo list-categories`
- [ ] Verify persistence: restart app, verify category loads correctly

**Checkpoint**: User Story 1 complete - users can organize and filter tasks by category

---

## Phase 4: User Story 2 - Tag Tasks with Multiple Labels (Priority: P2)

**Goal**: Users can apply multiple tags to tasks and filter by individual tags

**Independent Test**:
1. Add task with `--tags urgent bug-fix`
2. Add task with `--tags meeting important`
3. Filter with `todo list --tag urgent`
4. Verify all urgent tasks shown (regardless of other tags)
5. Verify tags displayed comma-separated in task list

**Acceptance Scenarios from Spec**:
- Given no tasks exist, When user creates task with tags ["urgent", "bug-fix"], Then task created with both tags
- Given 10 tasks with various tags, When user filters by "urgent", Then all tasks with "urgent" displayed
- Given task with tags ["review", "code"], When user adds "urgent", Then task has three tags
- Given multiple tasks, When user lists tags, Then all distinct tags displayed

### Implementation for User Story 2

- [ ] T020 [P] [US2] Add --tags argument (nargs='*') to 'add' command parser in src/main.py
- [ ] T021 [P] [US2] Add --tags argument to 'update' command parser in src/main.py
- [ ] T022 [P] [US2] Add --tag filter argument to 'list' command parser in src/main.py
- [ ] T023 [US2] Update cmd_add() to pass tags parameter to add_task() in src/main.py
- [ ] T024 [US2] Update cmd_update() to handle tags parameter (including "none" for clearing) in src/main.py
- [ ] T025 [US2] Update cmd_list() to apply tag filter using get_tasks_by_tag() in src/main.py
- [ ] T026 [P] [US2] Add "Tags" column to task list table with comma-separated display in src/ui/console.py
- [ ] T027 [P] [US2] Implement tag truncation (max 5 tags, "..." for overflow) in src/ui/console.py
- [ ] T028 [P] [US2] Display tags in format_task_created() output in src/ui/console.py
- [ ] T029 [P] [US2] Display tags changes in format_task_updated() output in src/ui/console.py
- [ ] T030 [US2] Add list-tags command parser in src/main.py
- [ ] T031 [US2] Implement cmd_list_tags() handler in src/main.py
- [ ] T032 [US2] Implement format_tags_list() in src/ui/console.py

**Manual Testing Checklist for US2**:
- [ ] Create task with tags: `todo add "Test task" --tags urgent bug-fix`
- [ ] Verify tags shown comma-separated
- [ ] Create task with multiple tags: `todo add "Meeting" --tags meeting important work`
- [ ] List by tag: `todo list --tag urgent`
- [ ] Verify filtering works (case-insensitive)
- [ ] Update tags: `todo update 1 --tags review code urgent`
- [ ] Verify duplicate tags removed: `todo add "Test" --tags urgent urgent`
- [ ] Clear tags: `todo update 1 --tags none`
- [ ] List all tags: `todo list-tags`
- [ ] Test tags with spaces: `todo add "Task" --tags "high priority" urgent`
- [ ] Verify persistence: restart app, verify tags load correctly

**Checkpoint**: User Story 2 complete - users can tag tasks with multiple labels and filter by tags

---

## Phase 5: User Story 3 - Combine Categories and Tags (Priority: P3)

**Goal**: Users can combine category and tag filters to narrow task lists precisely

**Independent Test**:
1. Add tasks with various category/tag combinations
2. Filter with `todo list --category work --tag urgent`
3. Verify only tasks matching BOTH criteria shown
4. Test each filter independently to verify they still work

**Acceptance Scenarios from Spec**:
- Given tasks in multiple categories with tags, When filter by category "work" AND tag "urgent", Then only matching tasks displayed
- Given mixed tasks, When user clears filters, Then all tasks displayed
- Given active filters, When apply new filter, Then filters combine (AND logic)

### Implementation for User Story 3

- [ ] T033 [US3] Update cmd_list() to support combined category + tag filtering (AND logic) in src/main.py
- [ ] T034 [US3] Handle filter intersection when both --category and --tag provided in src/main.py
- [ ] T035 [US3] Update task list output to show active filters in header in src/ui/console.py

**Manual Testing Checklist for US3**:
- [ ] Create diverse tasks: work+urgent, work+meeting, personal+urgent, personal+shopping
- [ ] Filter by category only: `todo list --category work` (should show work+urgent and work+meeting)
- [ ] Filter by tag only: `todo list --tag urgent` (should show work+urgent and personal+urgent)
- [ ] Combined filter: `todo list --category work --tag urgent` (should show only work+urgent)
- [ ] Verify empty results handled: `todo list --category nonexistent --tag nonexistent`
- [ ] Verify case-insensitive: `todo list --category Work --tag Urgent`

**Checkpoint**: User Story 3 complete - users can combine filters for precise task discovery

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Final touches and validation across all user stories

- [ ] T036 [P] Update help text for all commands with category/tag examples in src/main.py
- [ ] T037 [P] Add error messages for edge cases (empty results, invalid task ID) in src/ui/console.py
- [ ] T038 Test quickstart.md examples end-to-end (run all commands from guide)
- [ ] T039 Verify backward compatibility (old tasks.json loads correctly with missing fields)
- [ ] T040 Test Rich table display with long category names and many tags (truncation)
- [ ] T041 Test Windows UTF-8 encoding with unicode characters in categories/tags
- [ ] T042 Code review: verify all validation rules implemented per data-model.md
- [ ] T043 Code review: verify all CLI contracts implemented per cli-contract.md

**Checkpoint**: Feature complete and polished - ready for commit and demo

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - verification tasks
- **Foundational (Phase 2)**: Depends on Setup verification - BLOCKS all user stories
- **User Stories (Phase 3-5)**: All depend on Foundational phase completion
  - US1 (P1) can proceed after Foundational
  - US2 (P2) can proceed after Foundational (independent of US1)
  - US3 (P3) depends on US1 and US2 being complete (combines their features)
- **Polish (Phase 6)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Depends on Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Depends on Foundational (Phase 2) - Independent of US1 (can develop in parallel)
- **User Story 3 (P3)**: Depends on US1 AND US2 completion - Integrates both filter types

### Within Each User Story

**Phase 3 (US1) - Category filtering**:
1. T008-T010 [P] - CLI argument parsers (parallel)
2. T011-T013 - Command handlers (sequential, depend on parsers)
3. T014-T016 [P] - UI display updates (parallel, independent of handlers)
4. T017-T019 - list-categories command (sequential after handlers)

**Phase 4 (US2) - Tag filtering**:
1. T020-T022 [P] - CLI argument parsers (parallel)
2. T023-T025 - Command handlers (sequential, depend on parsers)
3. T026-T029 [P] - UI display updates (parallel, independent of handlers)
4. T030-T032 - list-tags command (sequential after handlers)

**Phase 5 (US3) - Combined filtering**:
1. T033-T034 - Update cmd_list() for AND logic (sequential)
2. T035 - UI filter display (depends on T033-T034)

### Parallel Opportunities

**Phase 1 (Setup)**: All 3 tasks can run in parallel - just file reads

**Phase 2 (Foundational)**: Tasks sequential (updating same file)

**Phase 3 (US1) Parallel Groups**:
- Group 1: T008, T009, T010 (different parsers)
- Group 2: T014, T015, T016 (different UI methods)

**Phase 4 (US2) Parallel Groups**:
- Group 1: T020, T021, T022 (different parsers)
- Group 2: T026, T027, T028, T029 (different UI methods)

**Phase 6 (Polish) Parallel Groups**:
- Group 1: T036, T037 (different concerns)

**Cross-Phase Parallelism**:
- US1 (Phase 3) and US2 (Phase 4) can be developed in parallel after Phase 2 completes
- US1 CLI work (T008-T013) can proceed while US1 UI work (T014-T016) happens in parallel
- US2 CLI work (T020-T025) can proceed while US2 UI work (T026-T029) happens in parallel

---

## Parallel Example: User Story 1 (Category Filtering)

```bash
# After Phase 2 completes, launch US1 CLI and UI work in parallel:

# Parallel Group 1 - CLI Argument Parsers:
Task: "Add --category argument to 'add' command parser in src/main.py"
Task: "Add --category argument to 'update' command parser in src/main.py"
Task: "Add --category filter argument to 'list' command parser in src/main.py"

# Parallel Group 2 - UI Display Updates (after Group 1 done):
Task: "Add Category column to task list table in src/ui/console.py"
Task: "Display category in format_task_created() output in src/ui/console.py"
Task: "Display category changes in format_task_updated() output in src/ui/console.py"
```

---

## Parallel Example: User Story 2 (Tag Filtering)

```bash
# After Phase 2 completes, launch US2 work (can run parallel with US1):

# Parallel Group 1 - CLI Argument Parsers:
Task: "Add --tags argument to 'add' command parser in src/main.py"
Task: "Add --tags argument to 'update' command parser in src/main.py"
Task: "Add --tag filter argument to 'list' command parser in src/main.py"

# Parallel Group 2 - UI Display Updates:
Task: "Add Tags column to task list table in src/ui/console.py"
Task: "Implement tag truncation in src/ui/console.py"
Task: "Display tags in format_task_created() output in src/ui/console.py"
Task: "Display tags changes in format_task_updated() output in src/ui/console.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (verify foundation - 3 tasks)
2. Complete Phase 2: Foundational (service signatures - 4 tasks)
3. Complete Phase 3: User Story 1 (category filtering - 12 tasks)
4. **STOP and VALIDATE**: Run manual testing checklist for US1
5. If passing, commit US1 as MVP: "feat: Add category filtering for task organization"
6. Demo: Show category assignment, filtering, and listing

### Incremental Delivery

1. **Foundation** (Phase 1-2): Verify model and update service layer → Foundation ready
2. **MVP** (Phase 3): Add category filtering → Test independently → Commit/Demo
3. **Enhancement** (Phase 4): Add tag filtering → Test independently → Commit/Demo
4. **Advanced** (Phase 5): Add combined filtering → Test independently → Commit/Demo
5. **Polish** (Phase 6): Final touches and cross-story validation → Final commit

Each phase adds value without breaking previous functionality.

### Parallel Team Strategy

With multiple developers:

1. Team completes Phase 1-2 together (foundation)
2. Once Phase 2 done:
   - **Developer A**: User Story 1 (Phase 3) - Category filtering
   - **Developer B**: User Story 2 (Phase 4) - Tag filtering
3. After both US1 and US2 complete:
   - **Either developer**: User Story 3 (Phase 5) - Combined filtering
4. Team completes Phase 6 (Polish) together

**Benefit**: US1 and US2 are independent - parallel development accelerates delivery

---

## Implementation Notes

### Task Count Summary

- **Total Tasks**: 43 tasks
- **Phase 1 (Setup)**: 3 tasks (verification)
- **Phase 2 (Foundational)**: 4 tasks (service layer)
- **Phase 3 (US1 - Category)**: 12 tasks (CLI + UI)
- **Phase 4 (US2 - Tags)**: 13 tasks (CLI + UI)
- **Phase 5 (US3 - Combined)**: 3 tasks (integration)
- **Phase 6 (Polish)**: 8 tasks (validation + refinement)

### Parallel Opportunities Identified

- **Phase 1**: 3 tasks can run in parallel
- **Phase 3**: 6 tasks can run in parallel (2 groups of 3)
- **Phase 4**: 7 tasks can run in parallel (2 groups)
- **Phase 6**: 2 tasks can run in parallel
- **Cross-phase**: US1 and US2 entire phases can run in parallel after Phase 2

### MVP Scope (Recommended First Delivery)

**Phases 1-3 only** (19 tasks total):
- Phase 1: Setup verification (3 tasks)
- Phase 2: Foundational service updates (4 tasks)
- Phase 3: User Story 1 - Category filtering (12 tasks)

**Why this is MVP**:
- Provides immediate value: organize tasks by area
- Complete user story: add, update, filter, list categories
- Independently testable and demonstrable
- Foundation for US2 and US3

**Estimated effort**: 2-4 hours for experienced developer

---

## Notes

- **[P] tasks**: Different files or independent methods, no dependencies
- **[Story] labels**: Maps task to user story for traceability (US1, US2, US3)
- **File paths**: All paths are specific to enable autonomous execution
- **Manual testing**: Checklist provided for each user story (no automated tests for hackathon)
- **Backward compatibility**: Phase 6 includes validation that old data loads correctly
- **Commit strategy**: Commit after each phase or logical group (US1, US2, US3 separately)
- **Stop points**: Each phase checkpoint allows validation before proceeding
- **Avoid**: Do not mix US1 and US2 tasks - keep stories independent until US3 integration

---

## Success Criteria (from Spec)

After completing all phases:

- ✅ **SC-001**: Users can assign category and tags in under 10 seconds (simple CLI flags)
- ✅ **SC-002**: Category filtering returns results instantly (<1 second for up to 1000 tasks)
- ✅ **SC-003**: Tag filtering returns results instantly (<1 second for up to 1000 tasks)
- ✅ **SC-004**: Display handles 20-char categories and 5 tags without truncation issues
- ✅ **SC-005**: 90% user success rate (intuitive CLI design with help text)
- ✅ **SC-006**: Filtering reduces visible tasks by 50% on average (effective organization)

All success criteria testable through manual validation with quickstart.md examples.
