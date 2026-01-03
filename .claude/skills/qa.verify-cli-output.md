---
description: Verify CLI output formatting, user experience, and adherence to output standards for the Todo App.
owner: qa-agent
---

## User Input

```text
$ARGUMENTS
```

## Skill: Verify CLI Output

Validate that all CLI commands produce correctly formatted, user-friendly output that meets the Todo App Phase 1 standards.

### Purpose

Ensure the Todo App CLI provides consistent, readable output across all commands, handles terminal display correctly, and follows established formatting conventions.

### When to Use

- After implementing a new CLI command
- When modifying output formatting code
- Before demo or presentation
- When users report display issues
- During UX review of CLI interactions

### Inputs

| Input | Required | Description |
|-------|----------|-------------|
| `command` | No | Specific command to verify: `add`, `list`, `update`, `delete`, `complete`, or `all` (default: `all`) |
| `terminal_width` | No | Simulated terminal width for wrapping tests (default: `80`) |

### Step-by-Step Process

1. **Verify Success Output Formatting**
   - Execute each command with valid inputs
   - Check output contains expected confirmation message
   - Verify task IDs are displayed consistently (format: `TODO-XXXX` or numeric)
   - Confirm timestamps use consistent format (ISO-8601 or human-readable)
   - Validate priority levels display correctly (low/medium/high/urgent)

2. **Verify List Command Output**
   - Check table/list alignment with varying title lengths
   - Verify column headers are present and aligned
   - Test with 0, 1, 5, and 20+ tasks
   - Confirm status indicators are clear (pending/completed symbols)
   - Verify due date formatting is consistent
   - Check sorting order is logical (by date, priority, or creation)

3. **Verify Error Output Formatting**
   - Trigger each known error condition
   - Verify errors output to stderr (not stdout)
   - Check error messages are user-friendly (no raw exceptions)
   - Confirm error messages include actionable guidance
   - Verify exit codes are non-zero for errors

4. **Verify Empty State Handling**
   - List tasks when none exist
   - Check for friendly "no tasks" message (not blank output)
   - Verify message guides user on how to add tasks

5. **Verify Input Echo/Feedback**
   - Confirm commands acknowledge user input
   - Check created tasks echo back key details
   - Verify updates show before/after where appropriate

6. **Verify Terminal Compatibility**
   - Test output at 80-column width (standard)
   - Test output at 120-column width (wide)
   - Check for proper line wrapping (no mid-word breaks)
   - Verify no ANSI codes if terminal doesn't support color

7. **Compile Verification Report**

### Output

```text
CLI Output Verification Report
==============================
Command Scope: [all|specific command]
Terminal Width: [width]
Timestamp: [ISO-8601]

Checks:
  [PASS] Success messages formatted correctly
  [PASS] List output aligned and readable
  [PASS] Error messages user-friendly
  [PASS] Empty states handled gracefully
  [PASS] Input feedback provided
  [WARN] Wide terminal wrapping needs review

Summary: [X/Y checks passed]
Status: [PASS|WARN|FAIL]

[If issues found, list with screenshots/examples]
```

### Failure Handling

| Failure Type | Action |
|--------------|--------|
| Output missing expected text | Log actual output, mark FAIL |
| Alignment issues detected | Capture output sample, mark WARN |
| Error sent to stdout | Mark FAIL, note stderr requirement |
| ANSI codes in plain terminal | Mark WARN, suggest fallback |
| Truncation without indicator | Mark FAIL, recommend ellipsis handling |

### Examples

Verify all CLI output:
```
/qa.verify-cli-output
```

Verify list command at narrow terminal:
```
/qa.verify-cli-output list --terminal_width=60
```

### Acceptance Criteria Reference

- All success messages start with action verb (Created, Updated, Deleted, Completed)
- Task IDs always visible in output for reference
- No stack traces shown to users
- Help text available for all commands
- Consistent date format throughout
