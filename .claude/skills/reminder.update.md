---
description: Reschedule or modify an existing reminder.
---

## User Input

```text
$ARGUMENTS
```

## Skill: Update Reminder

Modify an existing reminder's time, recurrence, or associated task.

### Instructions

1. **Identify the reminder**:
   - Parse reminder ID or description
   - If ambiguous, show matching reminders and ask for clarification
   - If not found, suggest similar reminders

2. **Parse updates**:
   - New time/date (parse natural language)
   - New recurrence pattern
   - Different associated task
   - Snooze duration (special case)

3. **Validate updates**:
   - Ensure new time is in the future
   - Validate recurrence pattern
   - Verify new task exists if changing association

4. **Apply updates**:
   - Update only specified fields
   - Reschedule notification trigger
   - Preserve reminder ID

5. **Confirm changes**:
   - Show before/after comparison:
     ```
     Reminder updated:
     - Time: [old time] → [new time]
     - Recurrence: [old] → [new]
     ```

### Snooze Shortcut

"Snooze [reminder] for 15 minutes":
- Find the reminder
- Set new time = now + snooze duration
- Set status to "snoozed"
- Confirm new trigger time

### Examples

User input: "Move my 2pm meeting reminder to 3pm"
- Find reminder with "meeting" at 2pm
- Update time to 3pm
- Confirm: "Reminder rescheduled: 2:00 PM → 3:00 PM"

User input: "Change medication reminder to 9am instead of 8am"
- Find "medication" reminder
- Update recurring time to 9:00 AM
- Confirm with new schedule
