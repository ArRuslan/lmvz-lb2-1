from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from simple_term_menu import TerminalMenu


@dataclass
class Group:
    name: str


@dataclass
class Deadline:
    group: Group
    date: datetime


@dataclass
class Task:
    name: str
    description: str
    deadlines: list[Deadline]


TASKS = [Task(f"Task {i}", "description", []) for i in range(1, 5)]
GROUPS = [Group(f"PZPI-22-{i}") for i in range(1, 11)]


def get_group_deadlines(g: Group) -> list[tuple[Task, Deadline]]:
    result = []
    for task in TASKS:
        result.extend([(task, d) for d in task.deadlines if d.group == g])
    return result


def get_group_tasks(g: Group) -> list[Task]:
    result = []
    for task in TASKS:
        if g in [d.group for d in task.deadlines]:
            result.append(task)
    return result


def get_date() -> Optional[datetime]:
    while True:
        date = input("Enter date (dd.mm.YYYY) or \"menu\" to return to menu: ").strip()
        if date == "menu":
            return
        try:
            date = datetime.strptime(date, "%d.%m.%Y")
        except ValueError:
            print("You have entered invalid date!")
            continue
        return date


def select_task_menu():
    tasks = [task.name for task in TASKS]
    tasks.append("Back")
    menu = TerminalMenu(tasks)
    task_idx = menu.show()
    if task_idx >= len(TASKS):
        return
    print(f"You have selected {tasks[task_idx]}!")
    select_group_menu(task_idx)


def select_group_menu(task_idx: int):
    task = TASKS[task_idx]
    lGROUPS = [group for group in GROUPS if task not in get_group_tasks(group)]
    groups = [group.name for group in lGROUPS]
    groups.append("To main menu")
    menu = TerminalMenu(groups)
    group_idx = menu.show()
    if group_idx >= len(lGROUPS):
        return
    group = lGROUPS[group_idx]
    print(f"You have selected {group.name}!")
    if (date := get_date()) is None:
        return
    task.deadlines.append(Deadline(group, date))
    print(f"Deadline for task \"{task.name}\" for group \"{group.name}\" set to {date.strftime('%d.%m.%Y')}!")


def show_groups_deadlines():
    groups = ["Clicking on any group will take you to main menu"]
    for group in GROUPS:
        groups.append(f" - Group: {group.name}, tasks")
        group_deadlines = get_group_deadlines(group)
        if group_deadlines:
            groups[-1] += f" ({len(group_deadlines)}):"
        for task, deadline in group_deadlines:
            groups.append(f"   * Task: {task.name}, deadline: {deadline.date.strftime('%d.%m.%Y')}")
    menu = TerminalMenu(groups)
    menu.show()


def main():
    while True:
        options = ["Add deadline", "View groups with deadlines", "Exit"]
        menu = TerminalMenu(options)
        option = menu.show()
        if option == 0:
            select_task_menu()
        elif option == 1:
            show_groups_deadlines()
        elif option == 2:
            break


if __name__ == '__main__':
    main()
