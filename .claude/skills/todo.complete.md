---
description: Mark a task as completed or toggle its completion status.
---

## User Input

```text
$ARGUMENTS
```

## Skill: Complete Task

Mark one or more tasks as completed.

### Instructions

1. **Identify the task(s)**:
   - Parse task identifier (ID or title match)
   - Support multiple tasks: "complete groceries and laundry"
   - If ambiguous, show matching tasks and ask for clarification

2. **Update status**:
   - Set status to "completed"
   - Set completion timestamp
   - Preserve other task properties

3. **Handle reminders**:
   - Cancel any pending reminders for completed tasks
   - Note cancelled reminders in response

4. **Confirm completion**:
   - Display: "Completed: [title]"
   - Show completion time
   - If multiple: show count and list

### Toggle Behavior

If a task is already completed and user says "complete [task]":
- Ask: "Task '[title]' is already completed. Reopen it?"
- On confirm: set status back to "pending", clear completion timestamp

### Examples

User input: "Done with groceries"
- Find task with "groceries"
- Mark as completed
- Display: "Completed: Buy groceries"

User input: "Mark T001, T002, and T003 as done"
- Find tasks by ID
- Mark all as completed
- Display: "Completed 3 tasks: [list titles]"

User input: "Finish the project report"
- Find task with "project report"
- Mark as completed
- Cancel any reminders
- Display: "Completed: Finish project report (reminder cancelled)"
