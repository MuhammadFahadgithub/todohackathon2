---
id: 002
title: Category Tag Filter Implementation Plan
stage: plan
date: 2026-01-04
surface: agent
model: claude-sonnet-4-5
feature: category-tag-filter
branch: 001-category-tag-filter
user: MuhammadFahadgithub
command: /sp.plan
labels: ["planning", "implementation", "architecture", "category", "tags", "filtering"]
links:
  spec: specs/001-category-tag-filter/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-category-tag-filter/plan.md
  - specs/001-category-tag-filter/research.md
  - specs/001-category-tag-filter/data-model.md
  - specs/001-category-tag-filter/contracts/cli-contract.md
  - specs/001-category-tag-filter/quickstart.md
tests:
  - Phase 0 research completed with 4 key decisions documented
  - Phase 1 design artifacts generated (data-model, contracts, quickstart)
  - Constitution check passed (no violations)
---

## Prompt

User continued Spec-Driven Development workflow after completing `/sp.specify`:

"uodate /sp,plan" (typo for "update /sp.plan")

Context: User had completed specification (`specs/001-category-tag-filter/spec.md`) with all validation checks passing. The specification defined 3 prioritized user stories (P1: categories, P2: tags, P3: combined filtering), 15 functional requirements, and 6 measurable success criteria. User requested implementation planning via `/sp.plan` to create detailed architecture and design artifacts.

## Response snapshot

**Implementation Plan Creation**:

Successfully completed `/sp.plan` workflow with all three phases:

**Phase 0: Research & Discovery** (`research.md` - 283 lines):

Generated comprehensive research document addressing 4 critical questions:

1. **R1: Case-Insensitive String Matching in Python**
   - Decision: Use `.lower()` comparison
   - Rationale: Simple, no dependencies, standard Python idiom
   - Implementation: `category.lower() == filter.lower()`

2. **R2: CLI Argument Parsing for Lists**
   - Decision: Space-separated with `nargs='*'`
   - Rationale: Most natural for CLI users, standard argparse pattern
   - Implementation: `--tags urgent bug-fix meeting`

3. **R3: Rich Table Display for Lists**
   - Decision: Comma-separated string with truncation
   - Rationale: Simple, works with existing Rich Table, readable
   - Implementation: `", ".join(task.tags[:5])`

4. **R4: Duplicate Tag Prevention**
   - Decision: Silent deduplication with set operations
   - Rationale: User-friendly, no errors for innocent mistakes
   - Implementation: `list(dict.fromkeys(t.lower() for t in tags))`

**Dependencies Analysis**:
- No new dependencies required
- Existing Rich 14.2.0 and python-dateutil sufficient
- Standard library (dataclasses, json, argparse, typing) covers all needs

**Integration Points** (5 documented):
- IP1: Task Model (✅ already extended)
- IP2: Persistence (✅ already updated)
- IP3: Service Layer (✅ filter methods added, ⏳ add_task signature pending)
- IP4: CLI Interface (⏳ argument parsers pending)
- IP5: Rich UI Display (⏳ table columns pending)

**Phase 1: Design & Architecture** (`plan.md` - 336 lines):

Created complete implementation plan with:

1. **Technical Context**:
   - Language: Python 3.14.0
   - Dependencies: Rich 14.2.0, python-dateutil
   - Storage: JSON file persistence (~/.todo_cli/tasks.json)
   - Testing: Manual CLI testing + optional pytest
   - Performance: Filter 1000 tasks in <1 second

2. **Constitution Check**: ✅ PASS
   - Simplicity first (no unnecessary abstractions)
   - Backward compatibility (optional fields with defaults)
   - User-friendly (clear CLI flags, helpful error messages)
   - Incremental development (P1→P2→P3 phased delivery)

3. **Project Structure**:
   - specs/001-category-tag-filter/ (spec, plan, research, data-model, contracts, quickstart, tasks.md)
   - src/ (main.py ⏳, console.py ⏳, todo_service.py ⏳, task.py ✅, persistence.py ✅)

4. **Implementation Priorities**:
   - P1 (MVP): CLI args, service signature updates, basic filtering
   - P2 (Better UX): Rich table columns, styled display
   - P3 (Nice-to-have): Combined filtering, list categories/tags commands

5. **Testing Strategy**:
   - Manual checklist (11 test cases)
   - Optional automated tests (unit + integration)

6. **Risk Assessment**:
   - Breaking JSON data (HIGH risk, mitigated with optional fields)
   - CLI argument conflicts (MEDIUM risk, mitigated with unique flag names)
   - Rich table width overflow (LOW risk, mitigated with truncation)

**Phase 1 Artifacts Generated**:

1. **data-model.md** (273 lines):
   - Extended Task entity with category and tags fields
   - Validation rules for both fields
   - JSON persistence format with backward compatibility
   - Query operations (5 supported queries)
   - No migration required (graceful degradation)

2. **contracts/cli-contract.md** (456 lines):
   - 5 command extensions documented:
     - `todo add` with `--category` and `--tags`
     - `todo update` with category/tags (including "none" for clearing)
     - `todo list` with `--category` and `--tag` filters
     - `todo list-categories` (NEW command)
     - `todo list-tags` (NEW command)
   - Argparse implementation details
   - Command handler pseudocode
   - Help text examples
   - Edge cases and error handling table
   - Backward compatibility notes

3. **quickstart.md** (336 lines):
   - Introduction and basic usage
   - Creating tasks with categories and tags
   - Filtering by category and tag
   - Combined filtering (P3)
   - Updating tasks
   - Discovering categories/tags with new commands
   - Common workflows (daily triage, weekly planning, project management)
   - Tips and best practices
   - Edge cases (spaces, case sensitivity, empty results)
   - Advanced examples

**Key Design Decisions**:

1. **Case-insensitive matching**: Aligns with user expectations, reduces typos
2. **Silent duplicate removal**: User-friendly, no errors for mistakes
3. **Space-separated tags**: Standard CLI pattern, no extra parsing
4. **Comma-separated display**: Simple Rich table integration
5. **No new dependencies**: Uses existing infrastructure
6. **Backward compatible JSON**: Old tasks load with defaults
7. **AND logic for combined filters**: More useful than OR for narrowing results

## Outcome

- ✅ Impact: Complete implementation plan with all Phase 0 and Phase 1 artifacts generated. Provides clear roadmap for CLI integration (main.py updates), service layer updates (add_task signature), and Rich UI enhancements (table columns). Ready for `/sp.tasks` to break down into actionable tasks.
- 🧪 Tests: Phase 0 research validated 4 design decisions. Phase 1 contracts define 11 manual test cases. Success metrics mapped to spec requirements (SC-001 through SC-006).
- 📁 Files: plan.md (336 lines), research.md (283 lines), data-model.md (273 lines), contracts/cli-contract.md (456 lines), quickstart.md (336 lines)
- 🔁 Next prompts: `/sp.tasks` to generate actionable task breakdown with acceptance criteria, then `/sp.implement` to execute tasks
- 🧠 Reflection: Planning after partial implementation is valuable - formalizes architectural decisions already made (model, persistence, service filters) and identifies remaining work clearly (CLI args, Rich UI display). The plan documents current state accurately (✅ vs ⏳) which helps prevent duplicate work. Phase 1 artifacts provide comprehensive reference for implementation (contracts as API spec, quickstart as user documentation, data-model as technical reference).

## Evaluation notes (flywheel)

- Failure modes observed: None - planning workflow followed SDD process successfully. PowerShell script had parameter error in previous session but was already resolved.
- Graders run and results (PASS/FAIL): PASS - Constitution check passed all criteria. All 4 research questions answered with clear decisions and rationale. Phase 1 artifacts complete with no placeholders remaining.
- Prompt variant (if applicable): Standard `/sp.plan` workflow following Phase 0 (research) → Phase 1 (design) structure
- Next experiment (smallest change to try): Consider generating code snippets in contracts for complex validation logic (e.g., duplicate tag removal algorithm) to reduce implementation interpretation errors. Current approach uses pseudocode which requires translation - actual Python code would be more precise for implementer.
