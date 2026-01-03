---
description: Set a reminder for a task at a specific date and time.
---

## User Input

```text
$ARGUMENTS
```

## Skill: Add Reminder

Schedule a reminder notification for a task.

### Instructions

1. **Parse reminder details**:
   - Task to remind about (ID, title, or description)
   - Reminder time (parse natural language):
     - "in 30 minutes", "in 2 hours"
     - "tomorrow at 9am"
     - "next Monday at 2pm"
     - "on January 15th at noon"
   - Recurrence (optional): daily, weekly, monthly, custom

2. **Validate the reminder**:
   - Ensure reminder time is in the future
   - Verify associated task exists (if specified)
   - Check for duplicate reminders at same time

3. **Create the reminder**:
   - Generate unique reminder ID
   - Store scheduled time in UTC
   - Link to task if applicable
   - Set status to "pending"

4. **Confirm creation**:
   - Display reminder details:
     ```
     Reminder set for [date] at [time]
     Task: [title]
     Recurrence: [pattern or "None"]
     Reminder ID: [id]
     ```

### Natural Language Parsing

- "remind me in 1 hour" → current time + 1 hour
- "remind me tomorrow morning" → tomorrow at 9:00 AM
- "remind me next week" → same time, 7 days from now
- "remind me every day at 8am" → daily recurrence

### Examples

User input: "Remind me about the meeting in 30 minutes"
- Task: (search for "meeting" task or create standalone reminder)
- Time: now + 30 minutes
- Create and confirm

User input: "Set a daily reminder for medication at 8am"
- Title: "Take medication"
- Time: 8:00 AM
- Recurrence: daily
- Create and confirm
