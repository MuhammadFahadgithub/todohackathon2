---
description: Add a new task to your todo list. Supports natural language for due dates and priorities.
---

## User Input

```text
$ARGUMENTS
```

## Skill: Add Task

Create a new task in the todo list based on the user's input.

### Instructions

1. **Parse the user input** to extract:
   - Task title (required)
   - Description (optional)
   - Due date (optional - parse natural language like "tomorrow", "next Friday", "in 3 days")
   - Priority (optional - low, medium, high, urgent; default: medium)
   - Tags (optional)

2. **Validate the task**:
   - Ensure title is provided and non-empty
   - Validate due date is in the future if specified
   - Normalize priority to allowed values

3. **Create the task**:
   - Generate a unique task ID
   - Set creation timestamp
   - Set status to "pending"
   - Store the task

4. **Confirm creation**:
   - Display: "Task created: [title] (ID: [id])"
   - Show due date and priority if set
   - Suggest setting a reminder if due date was specified

### Examples

User input: "Buy groceries tomorrow"
- Title: "Buy groceries"
- Due: [tomorrow's date]
- Priority: medium (default)

User input: "Finish project report by Friday, high priority"
- Title: "Finish project report"
- Due: [next Friday]
- Priority: high

User input: "Call mom"
- Title: "Call mom"
- Due: none
- Priority: medium (default)
