---
description: Delete a task or multiple tasks from your todo list.
---

## User Input

```text
$ARGUMENTS
```

## Skill: Delete Task

Remove task(s) from the todo list with confirmation.

### Instructions

1. **Identify target task(s)**:
   - Parse task identifier (ID or title match)
   - For bulk delete, parse criteria (e.g., "all completed", "older than 30 days")
   - If ambiguous, show matching tasks and ask for clarification

2. **Request confirmation**:
   - Single task: "Delete task '[title]' (ID: [id])? This cannot be undone."
   - Bulk delete: "Delete X tasks matching '[criteria]'? This cannot be undone."
   - List tasks that will be deleted

3. **On confirmation**:
   - Remove the task(s) from storage
   - Cancel any associated reminders

4. **Confirm deletion**:
   - Display: "Deleted: [title]" or "Deleted X tasks"
   - Show summary of what was removed

### Safety Checks

- Always require explicit confirmation before deletion
- For bulk deletes, show preview of affected tasks
- Never auto-delete without user consent
- Warn if deleting in-progress tasks

### Examples

User input: "Delete the groceries task"
- Find task with "groceries"
- Ask: "Delete 'Buy groceries' (T005)?"
- On confirm: remove and confirm

User input: "Remove all completed tasks"
- Find all tasks with status: completed
- Show count and preview
- Ask: "Delete 8 completed tasks?"
- On confirm: remove all and confirm

User input: "Delete T003"
- Find task by exact ID
- Confirm and delete
