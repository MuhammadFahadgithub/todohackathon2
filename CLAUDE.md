# Claude Code Workflow: Evolution of Todo

This repository follows Spec-Driven Development (SDD) principles.

## Structure
- `/src`: Application source code.
- `/specs`: Vertical feature specifications, implementation plans, and task lists.
- `/history/prompts`: Prompt History Records (PHRs) for every major interaction.
- `.specify/memory`: Core project principles and agent context.

## Workflow Commands
- `/sp.constitution`: Update the project constitution.
- `/sp.specify`: Generate a functional specification for a new feature.
- `/sp.plan`: Design an implementation plan.
- `/sp.tasks`: Decompose the plan into atomic tasks.
- `/sp.implement`: Execute the task list.

## Commit Guidelines
Use the following prefix style:
- `feat:` for new features (e.g., `feat: US2 complete/delete`)
- `fix:` for bug fixes
- `docs:` for documentation updates
- `spec:` for SDD artifact updates
- `refactor:` for code restructuring
