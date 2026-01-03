---
description: Execute acceptance tests against Todo App features to validate they meet defined acceptance criteria from specifications.
owner: qa-agent
---

## User Input

```text
$ARGUMENTS
```

## Skill: Run Acceptance Tests

Execute end-to-end acceptance tests that validate Todo App features against their specification acceptance criteria.

### Purpose

Systematically verify that implemented features satisfy all acceptance criteria defined in feature specifications, ensuring the Todo App meets user requirements before release.

### When to Use

- After completing implementation of a feature
- Before marking a spec task as "done"
- During `/sp.implement` completion verification
- Before creating a pull request
- When validating bug fixes against original acceptance criteria

### Inputs

| Input | Required | Description |
|-------|----------|-------------|
| `feature` | No | Feature name to test (e.g., `add-todo`, `list-todos`). Default: all features |
| `spec_path` | No | Path to spec file. Default: `specs/<feature>/spec.md` |
| `criteria` | No | Specific acceptance criterion ID to test (e.g., `AC-1`). Default: all |

### Step-by-Step Process

1. **Load Acceptance Criteria**
   - Read spec file from `specs/<feature>/spec.md`
   - Parse acceptance criteria section
   - Extract each criterion with its ID and description
   - Build test checklist

2. **Initialize Test Environment**
   - Start fresh Todo App instance
   - Clear any existing data
   - Verify clean state

3. **Execute Each Acceptance Criterion**

   For each criterion (AC-X):

   a. **Parse the criterion** into:
      - Given (preconditions)
      - When (action)
      - Then (expected outcome)

   b. **Setup preconditions**
      - Create required test data
      - Set application state as specified

   c. **Execute the action**
      - Run the specified command/operation
      - Capture all output and state changes

   d. **Verify expected outcome**
      - Check output matches expectation
      - Verify state changes occurred
      - Validate side effects (if any)

   e. **Record result**
      - PASS: All expectations met
      - FAIL: One or more expectations not met
      - SKIP: Preconditions cannot be established
      - BLOCK: Depends on failing criterion

4. **Test Edge Cases from Spec**
   - Execute any documented edge cases
   - Verify error handling matches spec
   - Test boundary conditions

5. **Generate Traceability Matrix**
   - Map each test to its acceptance criterion
   - Identify any untested criteria
   - Flag criteria without clear test path

6. **Compile Test Report**

### Output

```text
Acceptance Test Report
======================
Feature: [feature-name]
Spec: [spec-path]
Timestamp: [ISO-8601]
Branch: [current-branch]

Acceptance Criteria Results:
----------------------------
[AC-1] [PASS] User can add a task with title only
       Given: Empty task list
       When: User runs 'todo add "Buy milk"'
       Then: Task created with title "Buy milk"

[AC-2] [PASS] User can add a task with due date
       Given: Empty task list
       When: User runs 'todo add "Meeting" --due tomorrow'
       Then: Task created with due date set to tomorrow

[AC-3] [FAIL] User sees error for empty title
       Given: Empty task list
       When: User runs 'todo add ""'
       Then: Error message displayed
       ACTUAL: No error shown, empty task created

[AC-4] [SKIP] Reminder notification sent
       REASON: Reminder feature not implemented in Phase 1

Summary:
--------
Total Criteria: 4
Passed: 2
Failed: 1
Skipped: 1
Blocked: 0

Coverage: 75% (3/4 testable criteria)
Status: FAIL

Action Required:
- Fix AC-3: Add validation for empty title
```

### Failure Handling

| Failure Type | Action |
|--------------|--------|
| Spec file not found | Report error, list available specs |
| Criterion unparseable | Mark SKIP, flag for spec review |
| Test throws exception | Capture error, mark as ERROR (not FAIL) |
| Flaky result (inconsistent) | Re-run 3x, mark FLAKY if inconsistent |
| Dependency failure | Mark dependent tests as BLOCKED |
| Timeout (>30s per criterion) | Mark TIMEOUT, continue next test |

### Examples

Run all acceptance tests for add-todo feature:
```
/qa.run-acceptance-tests add-todo
```

Run specific acceptance criterion:
```
/qa.run-acceptance-tests add-todo --criteria=AC-2
```

Run with custom spec path:
```
/qa.run-acceptance-tests --spec_path=specs/custom/my-feature.md
```

### Integration Points

- Reads specs from: `specs/<feature>/spec.md`
- Reports link to: `history/prompts/<feature>/`
- Supports `/sp.implement` completion verification
- Results can trigger `/sp.tasks` status updates
