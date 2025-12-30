import sys
from src.services.todo import TaskService
from src.ui.console import ConsoleUI

def get_int_input(prompt: str) -> int:
    while True:
        try:
            return int(input(prompt).strip())
        except ValueError:
            print("[ERROR] Please enter a valid numeric ID.")

def main():
    service = TaskService()
    ui = ConsoleUI()

    ui.display_welcome()

    while True:
        try:
            choice = ui.prompt_menu()

            if choice == 'A':
                title = input("Enter task title: ").strip()
                desc = input("Enter description (optional): ").strip()
                task = service.add_task(title, desc)
                ui.show_message(f"Task '{task.title}' added with ID {task.id}")

            elif choice == 'L':
                tasks = service.list_tasks()
                ui.display_tasks(tasks)

            elif choice == 'C':
                task_id = get_int_input("Enter task ID to toggle completion: ")
                task = service.toggle_task(task_id)
                status = "Completed" if task.is_completed else "Incomplete"
                ui.show_message(f"Task {task_id} is now {status}")

            elif choice == 'D':
                task_id = get_int_input("Enter task ID to delete: ")
                service.delete_task(task_id)
                ui.show_message(f"Task {task_id} deleted successfully.")

            elif choice == 'U':
                task_id = get_int_input("Enter task ID to update: ")
                # Check for existence implicitly or explicitly
                title = input("Enter new title (leave blank to keep current): ").strip()
                desc = input("Enter new description (leave blank to keep current): ").strip()

                updated_title = title if title else None
                updated_desc = desc if desc else None

                task = service.update_task(task_id, updated_title, updated_desc)
                ui.show_message(f"Task {task_id} updated successfully.")

            elif choice == 'E':
                print("\nGoodbye!")
                break

            else:
                ui.show_message("Command not recognized.", is_error=True)

        except ValueError as e:
            ui.show_message(str(e), is_error=True)
        except KeyError as e:
            ui.show_message(str(e).strip("'"), is_error=True)
        except Exception as e:
            ui.show_message(f"An unexpected error occurred: {e}", is_error=True)

if __name__ == "__main__":
    main()
