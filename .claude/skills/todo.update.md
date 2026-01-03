---
description: Update an existing task's title, description, due date, priority, or status.
---

## User Input

```text
$ARGUMENTS
```

## Skill: Update Task

Modify properties of an existing task.

### Instructions

1. **Identify the task**:
   - Parse task identifier from user input (ID or title match)
   - If ambiguous, show matching tasks and ask for clarification
   - If not found, suggest similar tasks (fuzzy match)

2. **Parse updates**:
   - New title
   - New description
   - New due date (parse natural language)
   - New priority (low, medium, high, urgent)
   - New status (pending, in-progress, completed, cancelled)

3. **Validate updates**:
   - Ensure new due date is valid if specified
   - Validate priority/status against allowed values
   - Preserve unchanged fields

4. **Apply updates**:
   - Update only specified fields
   - Set modified timestamp
   - Preserve creation timestamp and ID

5. **Confirm changes**:
   - Show before/after comparison
   - Display: "Task updated: [title]"
   - List each changed field with old → new values

### Examples

User input: "Change groceries task to high priority"
- Find task with "groceries" in title
- Update priority: medium → high

User input: "Move project deadline to next Monday"
- Find task with "project" in title
- Update due date to next Monday

User input: "Mark T003 as in progress"
- Find task by ID T003
- Update status: pending → in-progress
