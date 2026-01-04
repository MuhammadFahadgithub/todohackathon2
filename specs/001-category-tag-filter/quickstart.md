# Quick Start: Category and Tag Filtering

**Feature**: 001-category-tag-filter
**Created**: 2026-01-04
**Status**: Ready for Implementation

## Introduction

This guide shows you how to use category and tag filtering to organize your tasks effectively. Categories help you group tasks into mutually exclusive areas (work, personal, etc.), while tags let you apply multiple cross-cutting labels (urgent, meeting, etc.).

## Basic Usage

### Creating Tasks with Categories

Assign a single category to organize tasks by area:

```bash
# Work task
todo add "Review pull request" --category work --priority high

# Personal task
todo add "Buy groceries" --category personal

# Shopping task
todo add "Get new shoes" --category shopping --priority low
```

**Output**:
```
✅ Task created successfully!

ID: 5
Title: Review pull request
Status: ⏳ Pending
Priority: 🔴 High
Category: work
Tags: -
Created: 2026-01-04 10:30:00
```

### Creating Tasks with Tags

Apply multiple tags for flexible organization:

```bash
# Single tag
todo add "Fix login bug" --tags urgent

# Multiple tags
todo add "Team meeting" --tags meeting important work

# Tags with category
todo add "Deploy hotfix" --category work --tags urgent deployment bug-fix
```

**Output**:
```
✅ Task created successfully!

ID: 8
Title: Deploy hotfix
Status: ⏳ Pending
Category: work
Tags: urgent, deployment, bug-fix
Created: 2026-01-04 11:15:00
```

## Filtering Tasks

### Filter by Category

Show only tasks in a specific category:

```bash
# Show all work tasks
todo list --category work

# Show personal tasks
todo list --category personal

# Case-insensitive
todo list --category Work  # Same as "work"
```

**Output**:
```
📋 Todo List (Filtered: category=work)

┏━━━━┳━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ ID ┃ Status    ┃ Priority┃ Category     ┃ Title                  ┃
┡━━━━╇━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━┩
│  5 │ ⏳ Pending│ 🔴 High │ work         │ Review pull request    │
│  8 │ ⏳ Pending│ 🟡 Med  │ work         │ Deploy hotfix          │
│ 12 │ ⏳ Pending│ 🟢 Low  │ work         │ Update documentation   │
└────┴───────────┴─────────┴──────────────┴────────────────────────┘

Showing 3 of 15 tasks
```

### Filter by Tag

Show all tasks with a specific tag:

```bash
# Show all urgent tasks
todo list --tag urgent

# Show meeting-related tasks
todo list --tag meeting

# Case-insensitive
todo list --tag Urgent  # Same as "urgent"
```

**Output**:
```
📋 Todo List (Filtered: tag=urgent)

┏━━━━┳━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ ID ┃ Status    ┃ Priority┃ Tags         ┃ Title                  ┃
┡━━━━╇━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━┩
│  7 │ ⏳ Pending│ 🔴 High │ urgent       │ Fix login bug          │
│  8 │ ⏳ Pending│ 🟡 Med  │ urgent, ...  │ Deploy hotfix          │
│ 10 │ ⏳ Pending│ 🔴 High │ urgent, ...  │ Client presentation    │
└────┴───────────┴─────────┴──────────────┴────────────────────────┘

Showing 3 of 15 tasks
```

### Combined Filtering (P3)

Combine category and tag filters to narrow results:

```bash
# Show urgent work tasks
todo list --category work --tag urgent

# Show personal tasks that are meetings
todo list --category personal --tag meeting
```

**Output**:
```
📋 Todo List (Filtered: category=work, tag=urgent)

┏━━━━┳━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ ID ┃ Status    ┃ Priority┃ Tags         ┃ Title                  ┃
┡━━━━╇━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━┩
│  8 │ ⏳ Pending│ 🟡 Med  │ urgent, ...  │ Deploy hotfix          │
└────┴───────────┴─────────┴──────────────┴────────────────────────┘

Showing 1 of 15 tasks
```

## Updating Tasks

### Update Category

Change a task's category:

```bash
# Move task to different category
todo update 5 --category personal

# Clear category (remove it)
todo update 5 --category none
```

**Output**:
```
✅ Task updated successfully!

Changes:
  Category: work → personal

ID: 5
Title: Review pull request
Status: ⏳ Pending
Category: personal
Created: 2026-01-04 10:30:00
```

### Update Tags

Replace all tags on a task:

```bash
# Replace tags
todo update 8 --tags urgent critical deployment

# Clear all tags
todo update 8 --tags none
```

**Output**:
```
✅ Task updated successfully!

Changes:
  Tags: [urgent, bug-fix, deployment] → [urgent, critical, deployment]

ID: 8
Title: Deploy hotfix
Status: ⏳ Pending
Tags: urgent, critical, deployment
Created: 2026-01-04 11:15:00
```

### Update Multiple Fields

Combine category/tag updates with other changes:

```bash
# Update priority, category, and tags together
todo update 5 --priority high --category work --tags urgent code-review
```

## Discovering Categories and Tags

### List All Categories

See which categories are currently in use:

```bash
todo list-categories
```

**Output**:
```
📂 Categories (4):

  • health
  • personal
  • shopping
  • work

Use: todo list --category <name>
```

### List All Tags

See which tags are currently in use:

```bash
todo list-tags
```

**Output**:
```
🏷️  Tags (7):

  • bug-fix
  • code-review
  • critical
  • deployment
  • meeting
  • review
  • urgent

Use: todo list --tag <name>
```

## Common Workflows

### Daily Task Triage

Review and organize your day:

```bash
# Check all urgent tasks across categories
todo list --tag urgent

# Review work tasks for today
todo list --category work --status pending

# See what meetings you have
todo list --tag meeting
```

### Weekly Planning

Organize tasks by area:

```bash
# Review all work tasks
todo list --category work

# Check personal errands
todo list --category personal

# Find high-priority items needing attention
todo list --priority high
```

### Project Management

Track bug fixes and features:

```bash
# Add bug with appropriate tags
todo add "Fix payment timeout" --category work --tags urgent bug-fix api --priority high

# Track feature work
todo add "Implement OAuth" --category work --tags feature authentication --priority medium

# List all bugs
todo list --tag bug-fix

# List all urgent work items
todo list --category work --tag urgent
```

## Tips and Best Practices

### Choosing Categories

**Good category examples**:
- `work` - Professional tasks
- `personal` - Personal errands and tasks
- `shopping` - Things to buy
- `health` - Medical appointments, fitness goals
- `finance` - Bills, budgeting, taxes
- `learning` - Courses, reading, skill development

**Keep it simple**: Use 3-7 categories maximum for easy management.

### Choosing Tags

**Good tag examples**:
- **Priority indicators**: `urgent`, `important`, `low-priority`
- **Task types**: `meeting`, `bug-fix`, `feature`, `review`, `research`
- **Context**: `home`, `office`, `phone-call`, `email`
- **Status**: `blocked`, `waiting`, `in-progress`
- **Projects**: `project-alpha`, `client-acme`, `q1-goals`

**Be consistent**: Reuse existing tags rather than creating similar ones.

### Avoiding Common Mistakes

❌ **Don't**: Create too many similar tags
```bash
# Bad: Too many variations
--tags urgent
--tags Urgent
--tags high-priority
--tags important
--tags critical
```

✅ **Do**: Use consistent, reusable tags
```bash
# Good: Clear, consistent tags
--tags urgent
--tags important
```

❌ **Don't**: Use category for multiple concepts
```bash
# Bad: Trying to encode too much in category
--category "work-urgent-meeting"
```

✅ **Do**: Use category for area, tags for attributes
```bash
# Good: Category for area, tags for attributes
--category work --tags urgent meeting
```

## Edge Cases

### Tags with Spaces

Quote tags that contain spaces:

```bash
# Single tag with spaces
todo add "Review architecture" --tags "high priority"

# Multiple tags, some with spaces
todo add "Plan sprint" --tags "sprint planning" meeting work
```

### Case Sensitivity

All matching is case-insensitive:

```bash
# These are all equivalent
todo list --category work
todo list --category Work
todo list --category WORK

# These find the same tag
todo list --tag urgent
todo list --tag Urgent
todo list --tag URGENT
```

### Empty Results

Filtering by non-existent category/tag returns empty list:

```bash
todo list --category nonexistent
```

**Output**:
```
📋 Todo List (Filtered: category=nonexistent)

No tasks found matching your filters.

Try:
  todo list               # View all tasks
  todo list-categories    # View available categories
  todo list-tags          # View available tags
```

### Special Characters

Categories and tags accept any characters:

```bash
# Special characters allowed
todo add "Bug #42" --category "Q1-2026" --tags "bug-fix" "v2.0"

# Emojis work too (if your terminal supports them)
todo add "Celebrate" --category "🎉 events" --tags "🎂 party"
```

## Advanced Examples

### Complex Task Organization

```bash
# Work project with multiple tags
todo add "Implement user authentication" \
  --category work \
  --tags feature authentication security api \
  --priority high \
  --due "2026-01-15"

# Personal task with context tags
todo add "Call dentist" \
  --category health \
  --tags phone-call urgent appointment \
  --priority medium

# Shopping with specific store tags
todo add "Buy ingredients for dinner" \
  --category shopping \
  --tags grocery whole-foods tonight \
  --due today
```

### Multi-Criteria Filtering

```bash
# Urgent work tasks that are pending
todo list --category work --tag urgent --status pending

# High-priority meetings
todo list --tag meeting --priority high

# Personal tasks due soon (combine with existing filters)
todo list --category personal --status pending
```

## Keyboard-Friendly Shortcuts

Use short flags for faster typing:

```bash
# Short form (faster)
todo add "Task" -c work -t urgent meeting -p high -d tomorrow

# Long form (more readable)
todo add "Task" --category work --tags urgent meeting --priority high --due tomorrow
```

## Next Steps

1. **Start organizing**: Add categories to your existing tasks
2. **Apply tags**: Tag tasks with attributes like "urgent" or "meeting"
3. **Experiment with filters**: Try different combinations to find what works
4. **Review regularly**: Use `list-categories` and `list-tags` to audit your organization

---

**Ready to start?** Try this:

```bash
# Add your first categorized task
todo add "Learn category filtering" --category personal --tags tutorial learning

# List it
todo list --category personal

# Success! 🎉
```
