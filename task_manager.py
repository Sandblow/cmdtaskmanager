# Command-Line Task Manager

#  ______     ______     __   __     _____     ______     __         ______     __     __    #
# /\  ___\   /\  __ \   /\ "-.\ \   /\  __-.  /\  == \   /\ \       /\  __ \   /\ \  _ \ \   #
# \ \___  \  \ \  __ \  \ \ \-.  \  \ \ \/\ \ \ \  __<   \ \ \____  \ \ \/\ \  \ \ \/ ".\ \  #
#  \/\_____\  \ \_\ \_\  \ \_\\"\_\  \ \____-  \ \_____\  \ \_____\  \ \_____\  \ \__/".~\_\ #
#   \/_____/   \/_/\/_/   \/_/ \/_/   \/____/   \/_____/   \/_____/   \/_____/   \/_/   \/_/ #

# Last Modified: [18.10.2023 - 17:55]

import datetime
import json
import os

TASKS_FILENAME = "tasks.json"
tasks = []
TASK_STATES = ["Not started", "Started", "Halfway", "Done"]

def load_tasks_from_file():
    """Load tasks from a file."""
    if os.path.exists(TASKS_FILENAME):
        with open(TASKS_FILENAME, 'r') as f:
            return json.load(f)
    return []

def save_tasks_to_file():
    """Save tasks to a file."""
    with open(TASKS_FILENAME, 'w') as f:
        json.dump(tasks, f)

def clear_all_tasks():
    """Clear all tasks after confirmation."""
    global tasks
    confirmation = input("Are you sure you want to clear all tasks? (yes/no): ")
    if confirmation.lower() != "yes":
        print("Action cancelled.")
        return
    tasks = []
    save_tasks_to_file()
    print("All tasks cleared successfully!")

def add_tasks():
    """Add new tasks."""
    while True:
        try:
            num_tasks = int(input("How many tasks do you want to add? "))
            break
        except ValueError:
            print("Invalid input! Please enter a valid number.")

    for _ in range(num_tasks):
        name = input("\nEnter the name of the task: ")
        deadline = input("Enter the deadline for the task (DD.MM.YYYY): ")
        try:
            deadline = datetime.datetime.strptime(deadline, "%d.%m.%Y").isoformat()
        except ValueError:
            print("Invalid date format. Please use DD.MM.YYYY")
            continue

        task = {
            "name": name,
            "deadline": deadline,
            "status": TASK_STATES[0]
        }

        tasks.append(task)

    save_tasks_to_file()
    print(f"\n{num_tasks} tasks added successfully!")

def edit_task():
    """Edit an existing task."""
    list_tasks()
    while True:
        try:
            task_num = int(input("\nEnter the number of the task you want to edit: "))
            if 1 <= task_num <= len(tasks):
                break
            else:
                print("Invalid task number!")
        except ValueError:
            print("Invalid input! Please enter a valid number.")

    current_task = tasks[task_num - 1]

    new_name = input(f"Current Name ('{current_task['name']}'). Enter new name or press enter to keep: ")
    if new_name:
        current_task['name'] = new_name

    new_deadline = input(f"Current Deadline ('{datetime.datetime.fromisoformat(current_task['deadline']).strftime('%d.%m.%Y')}'). Enter new deadline (DD.MM.YYYY) or press enter to keep: ")
    if new_deadline:
        try:
            current_task['deadline'] = datetime.datetime.strptime(new_deadline, "%d.%m.%Y").isoformat()
        except ValueError:
            print("Invalid date format. Keeping the original deadline.")

    print("Select a new status:")
    for idx, state in enumerate(TASK_STATES, 1):
        print(f"{idx}. {state}")
    while True:
        try:
            state_choice = int(input())
            if 1 <= state_choice <= len(TASK_STATES):
                current_task['status'] = TASK_STATES[state_choice - 1]
                break
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Invalid input. Please try again.")

    save_tasks_to_file()
    print("\nTask updated successfully!")

def list_tasks():
    """List all the tasks."""
    if not tasks:
        print("No tasks available.")
        return

    for index, task in enumerate(tasks, start=1):
        deadline = datetime.datetime.fromisoformat(task['deadline']).strftime("%d.%m.%Y")
        print(f"{index}. {task['name']} (Deadline: {deadline}) - {task['status']}")

def delete_task():
    """Delete a task."""
    list_tasks()
    while True:
        try:
            task_num = int(input("Enter the number of the task you want to delete: "))
            if 1 <= task_num <= len(tasks):
                break
            else:
                print("Invalid task number!")
        except ValueError:
            print("Invalid input! Please enter a valid number.")

    del tasks[task_num - 1]
    save_tasks_to_file()
    print("Task deleted successfully!")

def main():
    """Main function to run the task manager."""
    global tasks
    tasks = load_tasks_from_file()

    while True:
        print("\nCommand-Line Task Manager")
        print("1. Add Tasks")
        print("2. List Tasks")
        print("3. Edit Task")
        print("4. Delete Task")
        print("5. Clear All Tasks")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_tasks()
        elif choice == "2":
            list_tasks()
        elif choice == "3":
            edit_task()
        elif choice == "4":
            delete_task()
        elif choice == "5":
            clear_all_tasks()
        elif choice == "6":
            break
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()
