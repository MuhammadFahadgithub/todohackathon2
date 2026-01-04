# Feature Specification: Category and Tag Filtering

**Feature Branch**: `001-category-tag-filter`
**Created**: 2026-01-04
**Status**: Draft
**Input**: User description: "category and tag filtering feature"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Organize Tasks by Category (Priority: P1)

Users need to organize their tasks into logical groups like "work", "personal", or "shopping" to better manage different areas of their life. Each task should belong to at most one category, allowing users to focus on related tasks together.

**Why this priority**: Essential foundation for task organization. Users need basic categorization before more advanced filtering. Without this, users must manually scan all tasks to find related items, which doesn't scale beyond 10-20 tasks.

**Independent Test**: Can be fully tested by creating tasks with categories and listing tasks by category. Delivers immediate value by allowing users to see only work-related tasks or only personal tasks.

**Acceptance Scenarios**:

1. **Given** no tasks exist, **When** user creates a task with category "work", **Then** task is created with the specified category
2. **Given** 5 tasks exist with mixed categories, **When** user filters by category "personal", **Then** only tasks with category "personal" are displayed
3. **Given** a task exists with category "work", **When** user updates its category to "personal", **Then** task category is changed and task appears in "personal" filter
4. **Given** multiple tasks exist, **When** user lists all unique categories, **Then** all distinct category names are displayed (e.g., "work", "personal", "shopping")

---

### User Story 2 - Tag Tasks with Multiple Labels (Priority: P2)

Users need to apply multiple descriptive labels (tags) to tasks for cross-cutting organization. For example, a task might be tagged with both "urgent" and "bug-fix" to indicate priority and type. This enables flexible filtering across different dimensions.

**Why this priority**: Builds on P1's single-category limitation. Allows users to mark tasks with multiple attributes without complex category hierarchies. Tags provide flexibility that categories alone cannot offer.

**Independent Test**: Can be tested by creating tasks with multiple tags and filtering by individual tags. Delivers value by enabling multi-dimensional task organization (e.g., find all "urgent" tasks across all categories).

**Acceptance Scenarios**:

1. **Given** no tasks exist, **When** user creates a task with tags ["urgent", "bug-fix"], **Then** task is created with both tags
2. **Given** 10 tasks with various tags, **When** user filters by tag "urgent", **Then** all tasks containing "urgent" tag are displayed regardless of other tags
3. **Given** a task with tags ["review", "code"], **When** user adds tag "urgent", **Then** task now has three tags ["review", "code", "urgent"]
4. **Given** multiple tasks exist, **When** user lists all unique tags, **Then** all distinct tag names used across tasks are displayed

---

### User Story 3 - Combine Categories and Tags for Filtering (Priority: P3)

Users want to combine category and tag filters to narrow down tasks efficiently. For example, show all "work" category tasks that are also tagged "urgent", or find all tasks tagged "meeting" regardless of category.

**Why this priority**: Enhances filtering power after basic category and tag support is working. Most users will find P1 and P2 sufficient initially, but power users benefit from combined filters.

**Independent Test**: Can be tested by filtering with both category and tags simultaneously. Delivers value by enabling precise task discovery (e.g., "show me urgent work items").

**Acceptance Scenarios**:

1. **Given** tasks exist in multiple categories with various tags, **When** user filters by category "work" AND tag "urgent", **Then** only tasks matching both criteria are displayed
2. **Given** mixed tasks, **When** user clears all filters, **Then** all tasks are displayed again
3. **Given** active filters, **When** user applies a new filter, **Then** filters combine to further narrow results (not replace previous filter)

---

### Edge Cases

- What happens when a user assigns an empty string or whitespace-only category?
  - System should treat empty/whitespace category as "no category"
- How does the system handle case sensitivity in categories and tags?
  - Categories and tags should be case-insensitive for matching (e.g., "Work" and "work" are the same)
- What happens when filtering by a category/tag that doesn't exist?
  - System should return an empty result list with a message like "No tasks found with category 'xyz'"
- How are duplicate tags handled?
  - System should prevent duplicate tags within the same task (e.g., adding "urgent" twice should result in only one "urgent" tag)
- What happens when listing categories/tags if no tasks exist?
  - System should return an empty list

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST allow users to assign an optional category to each task
- **FR-002**: System MUST allow users to assign zero or more tags to each task
- **FR-003**: System MUST provide a filter to list tasks by specific category
- **FR-004**: System MUST provide a filter to list tasks containing a specific tag
- **FR-005**: System MUST display category and tags when showing task details
- **FR-006**: System MUST allow users to update task category and tags after creation
- **FR-007**: System MUST allow users to remove category from a task
- **FR-008**: System MUST allow users to add tags to existing tasks
- **FR-009**: System MUST allow users to remove tags from existing tasks
- **FR-010**: System MUST list all unique categories currently used across tasks
- **FR-011**: System MUST list all unique tags currently used across tasks
- **FR-012**: System MUST perform case-insensitive matching for categories and tags
- **FR-013**: System MUST prevent duplicate tags within the same task
- **FR-014**: System MUST persist category and tags data when tasks are saved
- **FR-015**: System MUST load category and tags data when tasks are retrieved

### Key Entities

- **Task**: Extended to include optional category (single string) and tags (list of strings). Category represents the primary classification (e.g., "work", "personal"). Tags represent additional attributes (e.g., "urgent", "bug-fix", "meeting").
- **Category**: String identifier representing a task group. One task can have zero or one category. Case-insensitive.
- **Tag**: String identifier representing a task attribute. One task can have multiple tags. Case-insensitive. No duplicates within a task.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can assign category and tags to tasks in under 10 seconds
- **SC-002**: Users can filter tasks by category and see results instantly (under 1 second for up to 1000 tasks)
- **SC-003**: Users can filter tasks by tag and see results instantly (under 1 second for up to 1000 tasks)
- **SC-004**: Category and tags display correctly in task lists without truncation (up to 20 character category name and 5 tags per task)
- **SC-005**: 90% of users successfully organize tasks using categories within first use
- **SC-006**: Filtering reduces visible tasks by at least 50% on average, making task management more efficient

## Scope *(mandatory)*

### In Scope

- Adding category field to tasks (single string, optional)
- Adding tags field to tasks (list of strings, zero or more)
- CLI commands to filter tasks by category
- CLI commands to filter tasks by tag
- CLI options to set category and tags when creating tasks
- CLI options to update category and tags for existing tasks
- Display category and tags in task lists and task details
- List all unique categories in use
- List all unique tags in use
- Case-insensitive category and tag matching
- Persistence of category and tags to JSON storage

### Out of Scope

- Category hierarchies or nested categories
- Tag autocomplete or suggestions
- Pre-defined category lists
- Tag colors or visual styling beyond text
- Combining filters with boolean operators (AND/OR/NOT) - this is P3 and may be deferred
- Tag statistics or analytics (e.g., most used tags)
- Category/tag renaming across all tasks
- Import/export of category and tag configurations

## Assumptions *(mandatory)*

- Users understand the difference between categories (single, mutually exclusive) and tags (multiple, cross-cutting)
- Category names will be short (typically 3-15 characters)
- Users will use 2-5 tags per task on average
- Tag names will be short (typically 3-10 characters)
- Case-insensitive matching is acceptable (users don't need "Work" and "work" as separate categories)
- Users can manually fix typos in categories/tags by updating individual tasks
- JSON storage can efficiently handle arrays of strings for tags

## Dependencies

- Existing Task model must support additional fields (category: Optional[str], tags: List[str])
- Existing persistence layer must serialize/deserialize new fields
- Existing CLI argument parser must support new options (--category, --tags)
- Existing Rich UI display logic must render category and tags

## Non-Goals

- Advanced tag management features (bulk renaming, merging tags)
- Tag cloud or visualization of tag usage
- Smart suggestions based on task content
- Integration with external task management systems
- Multi-user tag sharing or collaboration features
- Tag-based notifications or reminders

## Open Questions

None - all requirements are clear and implementable with reasonable defaults.
