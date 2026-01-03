---
description: List and view your tasks with optional filtering by status, priority, date, or search term.
---

## User Input

```text
$ARGUMENTS
```

## Skill: List Tasks

Display tasks from the todo list with optional filtering and sorting.

### Instructions

1. **Parse filter criteria** from user input:
   - Status filter: pending, in-progress, completed, all (default: pending + in-progress)
   - Priority filter: low, medium, high, urgent
   - Date filter: today, tomorrow, this week, overdue, specific date
   - Search term: text to match in title/description
   - Tag filter: specific tags

2. **Retrieve matching tasks**:
   - Apply all specified filters
   - Sort by due date (ascending), then priority (descending)

3. **Display results**:
   - Show count: "Found X task(s)"
   - For each task, display:
     ```
     [ID] Title
         Priority: [priority] | Due: [date] | Status: [status]
         Description: [if present]
         Tags: [if present]
     ```
   - Group by date if multiple days
   - Highlight overdue tasks

4. **Handle empty results**:
   - If no tasks match: "No tasks found matching your criteria"
   - Suggest broadening the filter

### Common Queries

- "all tasks" → show all regardless of status
- "completed" → show only completed tasks
- "high priority" → filter by priority
- "overdue" → due date < today AND not completed
- "today" → due today
- "this week" → due within 7 days
