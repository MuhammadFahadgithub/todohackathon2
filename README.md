# Evolution of Todo (Phase I)

This is a simple, clean, and reliable command-line Todo application built as part of Phase I of the Evolution of Todo project.

## Features
- **Add Task**: Create new tasks with a title and optional description.
- **List Tasks**: View all tasks with their current status.
- **Complete Task**: Toggle the completion status of a task by ID.
- **Delete Task**: Remove tasks permanently by ID.
- **Update Task**: Modify the title or description of existing tasks.

## Tech Stack
- **Python 3.13+**
- **UV** for environment and dependency management.

## Setup & Usage

1. **Install UV** (if not already installed):
   Follow instructions at [astral.sh/uv](https://astral.sh/uv).

2. **Run the application**:
   ```bash
   uv run python src/main.py
   ```

3. **Follow the on-screen menu**:
   - `A`: Add a task
   - `L`: List tasks
   - `C`: Mark as complete/incomplete
   - `D`: Delete a task
   - `U`: Update a task
   - `E`: Exit

## Principles
- **In-Memory Storage**: No tasks are saved to disk. Data is lost when the app exits.
- **Separation of Concerns**: UI, Service Logic, and Data Models are cleanly separated.
- **ID Immutability**: Task IDs are unique and fixed once created.
