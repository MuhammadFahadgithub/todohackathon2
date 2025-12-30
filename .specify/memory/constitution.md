<!--
Sync Impact Report:
Version change: [0.0.0] → 1.0.0 (Initial major version based on Spec-Kit Plus Constitution)
Modified principles:
- [PRINCIPLE_1_NAME] → Clean Code (readable, maintainable, minimal complexity)
- [PRINCIPLE_2_NAME] → Separation of Concerns
- [PRINCIPLE_3_NAME] → Single Responsibility
- [PRINCIPLE_4_NAME] → Predictable Behavior (No hidden side effects)
- [PRINCIPLE_5_NAME] → Reliable Input Handling
Added sections:
- Scope & Vision
- Architecture Constraints
- Technology Constraints
- Project Structure
- Out-of-Scope (Explicitly Forbidden)
Removed sections: None
Templates requiring updates:
- .specify/templates/plan-template.md (✅ updated)
- .specify/templates/spec-template.md (✅ updated)
- .specify/templates/tasks-template.md (✅ updated)
Follow-up TODOs: None
-->

# Evolution of Todo Constitution

## Purpose & Vision
This project simulates the real-world evolution of software systems. In Phase I, the goal is to build a simple, clean, and reliable command-line Todo application that stores tasks in memory.

## Scope of Phase I
The system MUST remain:
- A console-based application
- In-memory only (no database, no file persistence)
- Single-user
- Synchronous execution

## Core Principles

### I. Clean Code
Implementations MUST be readable, maintainable, and avoid unnecessary complexity.

### II. Separation of Concerns
Business logic MUST be strictly separated from input/output (console) logic.

### III. Single Responsibility
Each function and module MUST have a single, well-defined responsibility.

### IV. Predictable Behavior
Code MUST have explicit and predictable behavior with no hidden side effects.

### V. Reliable Input Handling
System MUST provide clear error messages for invalid user input and gracefully handle invalid IDs.

## Architecture Constraints
- Tasks MUST be stored in an in-memory data structure (e.g., list or dict).
- Console interaction MUST be simple and user-friendly.
- No external databases or frameworks.

## Technology Constraints
- Python 3.13+
- UV for environment and dependency management.
- Spec-Kit Plus for specification-driven development.
- Claude Code as the AI coding assistant.

## Project Structure
The repository MUST include:
- `/src` — Python source code
- `/specs-history` — All generated and evolved specification files
- `/sp.constitution.md` — This constitution (symlink or copy)
- `README.md` — Setup and usage instructions
- `CLAUDE.md` — Instructions for working with Claude Code

## Governance
This constitution establishes the foundational rules for Phase I of the Evolution of Todo project. All development tasks, specifications, and plans MUST align with these principles and constraints.

Amendments to this constitution require a version bump following semantic versioning:
- MAJOR: Backward incompatible governance or principle removals.
- MINOR: New principles or sections added.
- PATCH: Clarifications and wording fixes.

**Version**: 1.0.0 | **Ratified**: 2025-12-30 | **Last Amended**: 2025-12-30
