"""Test script for due date functionality."""

import sys
import io
from datetime import datetime, timedelta
from src.services.todo_service import TodoService
from src.services.persistence import JsonPersistence

# Fix Windows console encoding for unicode characters
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def print_section(title):
    """Print a test section header."""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

def test_add_with_due_dates():
    """Test adding tasks with various due date formats."""
    print_section("TEST 1: Adding Tasks with Due Dates")

    service = TodoService()

    # Test 1: ISO format date
    task1, error1 = service.add_task("Buy groceries", due_date="2026-01-15")
    if task1:
        print(f"✓ ISO format: Task #{task1.id} - '{task1.title}'")
        print(f"  Due: {task1.due_date.strftime('%Y-%m-%d %H:%M:%S') if task1.due_date else 'None'}")
    else:
        print(f"✗ ISO format failed: {error1}")

    # Test 2: Natural language - "tomorrow"
    task2, error2 = service.add_task("Team meeting", priority="high", due_date="tomorrow")
    if task2:
        print(f"\n✓ Natural language 'tomorrow': Task #{task2.id} - '{task2.title}'")
        print(f"  Due: {task2.due_date.strftime('%Y-%m-%d %H:%M:%S') if task2.due_date else 'None'}")
        expected = (datetime.now() + timedelta(days=1)).date()
        actual = task2.due_date.date() if task2.due_date else None
        print(f"  Expected date: {expected}, Actual: {actual}, Match: {expected == actual}")
    else:
        print(f"\n✗ Tomorrow failed: {error2}")

    # Test 3: Natural language - relative date
    task3, error3 = service.add_task("Review code", due_date="next friday")
    if task3:
        print(f"\n✓ Natural language 'next friday': Task #{task3.id} - '{task3.title}'")
        print(f"  Due: {task3.due_date.strftime('%Y-%m-%d %H:%M:%S') if task3.due_date else 'None'}")
    else:
        print(f"\n✗ Next friday failed: {error3}")

    # Test 4: No due date
    task4, error4 = service.add_task("Call dentist")
    if task4:
        print(f"\n✓ No due date: Task #{task4.id} - '{task4.title}'")
        print(f"  Due: {task4.due_date if task4.due_date else 'None'}")
    else:
        print(f"\n✗ No due date failed: {error4}")

    # Test 5: Invalid due date
    task5, error5 = service.add_task("Invalid task", due_date="not-a-date-xyz123")
    if task5:
        print(f"\n✗ Invalid date should have failed but created: Task #{task5.id}")
    else:
        print(f"\n✓ Invalid date correctly rejected: {error5}")

    return service

def test_update_due_dates(service):
    """Test updating task due dates."""
    print_section("TEST 2: Updating Task Due Dates")

    # Add a task without due date
    task, _ = service.add_task("Write documentation")
    print(f"Created Task #{task.id}: '{task.title}'")
    print(f"Initial due date: {task.due_date if task.due_date else 'None'}")

    # Test 1: Add a due date
    updated_task, changes, error = service.update_task(task.id, due_date="2026-01-20")
    if updated_task and not error:
        print(f"\n✓ Added due date: {updated_task.due_date.strftime('%Y-%m-%d')}")
        print(f"  Changes: {changes}")
    else:
        print(f"\n✗ Failed to add due date: {error}")

    # Test 2: Update to a different date
    updated_task, changes, error = service.update_task(task.id, due_date="2026-02-01")
    if updated_task and not error:
        print(f"\n✓ Updated due date: {updated_task.due_date.strftime('%Y-%m-%d')}")
        print(f"  Changes: {changes}")
    else:
        print(f"\n✗ Failed to update due date: {error}")

    # Test 3: Update with natural language
    updated_task, changes, error = service.update_task(task.id, due_date="tomorrow")
    if updated_task and not error:
        print(f"\n✓ Updated with 'tomorrow': {updated_task.due_date.strftime('%Y-%m-%d')}")
        print(f"  Changes: {changes}")
    else:
        print(f"\n✗ Failed to update with natural language: {error}")

def test_clear_due_dates(service):
    """Test clearing due dates."""
    print_section("TEST 3: Clearing Due Dates")

    # Add a task with a due date
    task, _ = service.add_task("Task with due date", due_date="2026-01-25")
    print(f"Created Task #{task.id}: '{task.title}'")
    print(f"Initial due date: {task.due_date.strftime('%Y-%m-%d') if task.due_date else 'None'}")

    # Test 1: Clear with "none"
    updated_task, changes, error = service.update_task(task.id, due_date="none")
    if updated_task and not error:
        print(f"\n✓ Cleared with 'none': {updated_task.due_date if updated_task.due_date else 'None'}")
        print(f"  Changes: {changes}")
    else:
        print(f"\n✗ Failed to clear: {error}")

    # Test 2: Add date back and clear with "clear"
    service.update_task(task.id, due_date="2026-01-30")
    print(f"\nRe-added due date: {service.get_task_by_id(task.id).due_date.strftime('%Y-%m-%d')}")

    updated_task, changes, error = service.update_task(task.id, due_date="clear")
    if updated_task and not error:
        print(f"✓ Cleared with 'clear': {updated_task.due_date if updated_task.due_date else 'None'}")
        print(f"  Changes: {changes}")
    else:
        print(f"✗ Failed to clear: {error}")

def test_invalid_due_dates(service):
    """Test invalid due date handling."""
    print_section("TEST 4: Invalid Due Date Handling")

    # Test 1: Invalid date in add_task
    task1, error1 = service.add_task("Invalid add", due_date="xyz-invalid-123")
    if task1:
        print(f"✗ Should have rejected invalid date but created task #{task1.id}")
    else:
        print(f"✓ Correctly rejected invalid date in add_task:\n  {error1}")

    # Test 2: Invalid date in update_task
    task2, _ = service.add_task("Valid task")
    updated_task, changes, error2 = service.update_task(task2.id, due_date="not-a-date")
    if updated_task and changes:
        print(f"\n✗ Should have rejected invalid date but updated task")
    else:
        print(f"\n✓ Correctly rejected invalid date in update_task:\n  {error2}")

def test_time_handling():
    """Test that times are set to end of day."""
    print_section("TEST 5: Time Handling (End of Day)")

    service = TodoService()

    # Add task with date (no time specified)
    task, _ = service.add_task("Check time", due_date="2026-01-15")
    if task and task.due_date:
        print(f"Task created with date '2026-01-15'")
        print(f"Full datetime: {task.due_date.strftime('%Y-%m-%d %H:%M:%S')}")
        if task.due_date.hour == 23 and task.due_date.minute == 59:
            print("✓ Time correctly set to 23:59:59 (end of day)")
        else:
            print(f"✗ Time should be 23:59:59 but got {task.due_date.hour}:{task.due_date.minute}")
    else:
        print("✗ Failed to create task")

def test_persistence():
    """Test due date persistence."""
    print_section("TEST 6: Due Date Persistence")

    import tempfile
    import os

    # Create temp file
    temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
    temp_file.close()

    try:
        # Create service with persistence
        persistence = JsonPersistence(temp_file.name)
        service1 = TodoService(persistence)

        # Add tasks with due dates
        task1, _ = service1.add_task("Persistent task 1", due_date="2026-01-20")
        task2, _ = service1.add_task("Persistent task 2", due_date="tomorrow")

        print(f"Created 2 tasks with due dates:")
        print(f"  Task #{task1.id}: {task1.due_date.strftime('%Y-%m-%d')}")
        print(f"  Task #{task2.id}: {task2.due_date.strftime('%Y-%m-%d')}")

        # Create new service instance to load from file
        service2 = TodoService(JsonPersistence(temp_file.name))
        loaded_tasks = service2.get_all_tasks()

        print(f"\nLoaded {len(loaded_tasks)} tasks from file:")
        matches = 0
        for task in loaded_tasks:
            print(f"  Task #{task.id}: '{task.title}' - Due: {task.due_date.strftime('%Y-%m-%d') if task.due_date else 'None'}")
            original = service1.get_task_by_id(task.id)
            if original and original.due_date and task.due_date:
                if original.due_date.date() == task.due_date.date():
                    matches += 1

        if matches == 2:
            print(f"\n✓ All due dates persisted correctly")
        else:
            print(f"\n✗ Due date persistence failed ({matches}/2 matched)")

    finally:
        # Cleanup
        os.unlink(temp_file.name)

def main():
    """Run all due date tests."""
    print("\n" + "="*60)
    print("  DUE DATE FUNCTIONALITY TEST SUITE")
    print("="*60)

    try:
        # Run tests
        service = test_add_with_due_dates()
        test_update_due_dates(service)
        test_clear_due_dates(service)
        test_invalid_due_dates(service)
        test_time_handling()
        test_persistence()

        print_section("TEST SUITE COMPLETED")
        print("All tests executed. Review results above.\n")

    except Exception as e:
        print(f"\n✗ Test suite failed with exception: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
