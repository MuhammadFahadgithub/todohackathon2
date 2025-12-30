from typing import List
from src.models.task import Task

class ConsoleUI:
    @staticmethod
    def display_welcome():
        print("\n" + "="*40)
        print("   EVOLUTION OF TODO - PHASE I")
        print("="*40)

    @staticmethod
    def display_tasks(tasks: List[Task]):
        if not tasks:
            print("\n[!] No tasks found.")
            return

        print("\n{:<5} {:<20} {:<10} {:<30}".format("ID", "TITLE", "STATUS", "DESCRIPTION"))
        print("-" * 70)
        for task in tasks:
            status = "[X]" if task.is_completed else "[ ]"
            print("{:<5} {:<20} {:<10} {:<30}".format(
                task.id,
                task.title[:18] + '..' if len(task.title) > 18 else task.title,
                status,
                task.description[:28] + '..' if len(task.description) > 28 else task.description
            ))

    @staticmethod
    def show_message(message: str, is_error: bool = False):
        prefix = "[ERROR]" if is_error else "[SUCCESS]"
        print(f"\n{prefix} {message}")

    @staticmethod
    def prompt_menu():
        print("\nCommands: [A]dd, [L]ist, [C]omplete, [D]elete, [U]pdate, [E]xit")
        return input("Choose action: ").strip().upper()
