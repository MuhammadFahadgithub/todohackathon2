---
description: View upcoming reminders or search through scheduled notifications.
---

## User Input

```text
$ARGUMENTS
```

## Skill: List Reminders

Display scheduled reminders with optional filtering.

### Instructions

1. **Parse filter criteria**:
   - Time range: today, tomorrow, this week, all
   - Status: pending, triggered, snoozed
   - Associated task (ID or title)
   - Default: show pending reminders for next 7 days

2. **Retrieve matching reminders**:
   - Apply filters
   - Sort by scheduled time (ascending)

3. **Display results**:
   - Show count: "You have X upcoming reminder(s)"
   - For each reminder:
     ```
     [Date] at [Time] ([Timezone])
        [Task/Reminder Title]
        Recurrence: [pattern or "None"]
        Status: [status]
        ID: [reminder-id]
     ```
   - Group by date for easier scanning

4. **Handle empty results**:
   - "No reminders scheduled for [time range]"
   - Suggest creating a reminder: "Use /reminder.add to set one"

### Query Examples

- "reminders" → all pending for next 7 days
- "reminders today" → due today only
- "all reminders" → including triggered/past
- "reminders for project task" → filtered by task
