---
description: Cancel or delete a scheduled reminder.
---

## User Input

```text
$ARGUMENTS
```

## Skill: Delete Reminder

Cancel and remove a scheduled reminder.

### Instructions

1. **Identify the reminder**:
   - Parse reminder ID or description
   - Support bulk deletion: "all reminders for [task]"
   - If ambiguous, show matching reminders and ask for clarification

2. **Request confirmation**:
   - Single: "Cancel reminder for '[title]' at [time]?"
   - Bulk: "Cancel X reminders? [list them]"

3. **On confirmation**:
   - Remove the reminder(s) from storage
   - Cancel scheduled notifications

4. **Confirm deletion**:
   - Display: "Reminder cancelled: [title] at [time]"
   - For recurring: "Cancelled all future occurrences"

### Handling Recurring Reminders

When deleting a recurring reminder, ask:
- "Cancel just this occurrence, or all future reminders?"
- Options:
  1. This occurrence only (skip this one, keep recurrence)
  2. All future occurrences (full cancellation)

### Examples

User input: "Cancel the meeting reminder"
- Find reminder with "meeting"
- Ask: "Cancel reminder for 'Team meeting' at 2:00 PM?"
- On confirm: delete and confirm

User input: "Stop all medication reminders"
- Find all reminders matching "medication"
- Ask: "Cancel 7 daily reminders for 'Take medication'?"
- On confirm: delete all and confirm

User input: "Remove reminder R005"
- Find by exact ID
- Confirm and delete
