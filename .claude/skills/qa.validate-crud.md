---
description: Validate all CRUD operations (Create, Read, Update, Delete) for the Todo App work correctly and maintain data integrity.
owner: qa-agent
---

## User Input

```text
$ARGUMENTS
```

## Skill: Validate CRUD Operations

Systematically test all task CRUD operations to ensure functional correctness and data integrity.

### Purpose

Verify that the Todo App's core CRUD operations function correctly, handle edge cases gracefully, and maintain data consistency across the in-memory storage.

### When to Use

- After implementing or modifying any CRUD operation
- Before marking a feature task as complete
- During regression testing after code changes
- When validating acceptance criteria for task management features

### Inputs

| Input | Required | Description |
|-------|----------|-------------|
| `operation` | No | Specific operation to test: `create`, `read`, `update`, `delete`, or `all` (default: `all`) |
| `verbose` | No | Show detailed test output (default: `false`) |

### Step-by-Step Process

1. **Setup Test Environment**
   - Initialize a fresh in-memory task store
   - Record initial state (should be empty)

2. **Test CREATE Operations**
   - Create task with valid title only
   - Create task with title, description, due date, priority
   - Attempt to create task with empty title (expect rejection)
   - Attempt to create task with invalid priority (expect rejection or normalization)
   - Verify each created task has unique ID and correct timestamps

3. **Test READ Operations**
   - List all tasks (verify count matches created)
   - Read single task by valid ID (verify all fields)
   - Read single task by invalid ID (expect graceful error)
   - Filter tasks by status (pending, completed)
   - Filter tasks by priority

4. **Test UPDATE Operations**
   - Update task title
   - Update task description
   - Update task due date
   - Update task priority
   - Update multiple fields simultaneously
   - Attempt update on non-existent task (expect graceful error)
   - Verify updated_at timestamp changes

5. **Test DELETE Operations**
   - Delete task by valid ID
   - Verify task no longer appears in list
   - Attempt delete on non-existent ID (expect graceful error)
   - Attempt delete on already-deleted task (expect graceful error)

6. **Test Data Integrity**
   - Perform mixed operations (create, update, delete sequence)
   - Verify task count remains accurate
   - Verify no orphaned or corrupted data

7. **Compile Results**
   - Count passed/failed tests
   - Document any failures with reproduction steps

### Output

```text
CRUD Validation Report
======================
Operation: [all|create|read|update|delete]
Timestamp: [ISO-8601]

Results:
  CREATE: [X/Y passed]
  READ:   [X/Y passed]
  UPDATE: [X/Y passed]
  DELETE: [X/Y passed]

Status: [PASS|FAIL]

[If FAIL, list failures with details]
```

### Failure Handling

| Failure Type | Action |
|--------------|--------|
| Test assertion fails | Log expected vs actual, continue remaining tests |
| Operation throws exception | Capture stack trace, mark test as ERROR, continue |
| Data corruption detected | HALT all tests, report critical failure |
| Timeout on operation | Mark as TIMEOUT (>5s threshold), continue |

### Examples

Test all operations:
```
/qa.validate-crud
```

Test only create operations with verbose output:
```
/qa.validate-crud create --verbose
```
