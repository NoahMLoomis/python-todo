import sys
import os
import exceptions as e
import command_line as cmd
from colorama import init, Fore


task_list = {}


class Task():
    def __init__(self, task_id, desc, priority=None, project=None, completed=False):
        self.task_id = task_id
        self.desc = desc
        self.priority = priority
        self.project = project
        self.completed = completed

    def get_write_string(self):
        return f'{self.task_id}~{self.desc}~{self.completed}~{self.priority}~{self.project}'

    def change_completed(self):
        self.completed = True

    def __str__(self):
        return f'{self.desc} {self.priority} {self.project}'


def ensure_created_file():
    if not os.path.isfile('tasks.txt'):
        open('tasks.txt', 'w').close()


def get_new_task_id():
    if len(list(task_list)) < 1:
        return 1
    return int(list(task_list.keys())[-1]) + 1


def verify_task_id(task_id):
    if task_id in task_list:
        return task_id
    raise e.TaskNotFoundException(
        f'{Fore.RED}No task was found with task_id: {task_id}')


def get_line():
    if len(sys.argv) > 1:
        line = sys.argv[1:]
    else:
        line = input("Please enter a command: ").split()
    return line


def get_desc(task):
    desc = ""
    for word in task:
        if word[0] != "!" and word[0] != "#":
            desc += word + " "
    return desc.strip()


def get_action(task):
    for word in task:
        if not word[0].isnumeric():
            return word


def get_project(task):
    for word in task:
        if word[0] == '#':
            return word[1:]
    return None


def get_priority(task):
    for word in task:
        if word[0] == '!':
            try:
                if int(word[1]) < 1 or int(word[1]) > 4:
                    raise e.InvalidInputException(
                        "Priority cannot be less than 0 or greater than 4")
                return word[1]
            except ValueError:
                print(f'{Fore.RED}Priority must be an int')
                raise e.TerminateProgramException
    return None


def get_todo_sorted_by_priority():
    return sorted({key: task_list[key] for key in task_list if task_list[key].completed == 'False'}.items(), key=lambda s: s[1].priority)


def val_action(action):
    if action == "add" or action == "upd" or action == "rem" or action == "done" or action == "list" or action == "purge":
        return action
    raise e.InvalidActionException(
        "Invalid action. Action can be add, upd, rem, done, list or purge")


def val_list_type(list_type):
    if len(list_type) > 1 or list_type[0] != "all" and list_type[0] != "todo":
        raise e.InvalidListTypeException(
            "Can only list of type 'all' or 'todo'")


def val_line_format(input):
    project_count = 0
    priority_count = 0
    if get_desc(input) == "":
        raise e.InvalidInputException("You must enter a description")

    for w, word in enumerate(input):
        if word[0] == "~":
            raise e.InvalidInputException(
                "Cannot include '~'")
        if word[0] == "!":
            priority_count += 1
        if word[0] == '#':
            project_count += 1
            if len(input)-1 > w:
                raise e.InvalidInputException(
                    "Invalid input, the input must be [action] [description] -optional ![priority] -optional #[project]")
    if project_count > 1 or priority_count > 1:
        raise e.InvalidInputException(
            "There can only be one project, and one priority. Both are optional")


def print_header():
    print(
        f'\n{"Completed":^10}|{"Description":^80}|{"Priority":^15}|{"Project":^15}|')
    print("----------------------------------------------------------------------------------------------------------------------------")


def print_all():
    for key in task_list:
        print(
            f'{task_list[key].completed:^10}|{task_list[key].desc:^80}|{task_list[key].priority:^15}|{task_list[key].project:^15}|')


def print_todo():
    for task in get_todo_sorted_by_priority():
        print(
            f'{task[1].completed:^10}|{task[1].desc:^80}|{task[1].priority:^15}|{task[1].project:^15}|')


def add_task(input):
    id = get_new_task_id()
    task_list[id] = Task(id, get_desc(
        input), get_priority(input), get_project(input))
    print(f'{Fore.GREEN}New Task with task_id {id} added')


def rem_task(task_id):
    try:
        found_task_id = verify_task_id(task_id)
        del task_list[found_task_id]
        print(f'{Fore.GREEN}Task removed with the task_id of {task_id}')
    except e.TaskNotFoundException as msg:
        print(msg)


def upd_task(task_id, changes):
    try:
        found_task_id = verify_task_id(task_id)
        new_priority = get_priority(changes) if get_priority(
            changes) != None else task_list[found_task_id].priority
        new_project = get_project(changes) if get_project(
            changes) != None else task_list[found_task_id].project

        task_list[found_task_id] = Task(found_task_id, get_desc(
            changes), new_priority, new_project, task_list[found_task_id].completed)
    except e.TaskNotFoundException as msg:
        print(msg)


def purge_task_list():
    for key in list(task_list):
        if task_list[key].completed == "True":
            task_list.pop(key)


def change_completion_status(task_id):
    try:
        found_task_id = verify_task_id(task_id)
        task_list[found_task_id].change_completed()
    except e.TaskNotFoundException as msg:
        print(msg)


def write_to_file():
    out_file = open('tasks.txt', 'w')
    for key in task_list:
        out_str = task_list.get(key).get_write_string()
        if list(task_list)[0] == key:
            out_file.write(out_str)
        else:
            out_file.write(f'\n{out_str}')


def init_task_list():
    task_file = open('tasks.txt')
    tasks = {}
    for t in task_file.readlines():
        list_task = t.split("~")
        id = list_task[0]
        desc = list_task[1]
        comp = list_task[2]
        priority = list_task[3]
        project = list_task[4].strip('\n')
        tasks[id] = Task(id, desc, priority, project, completed=comp)
    return tasks


if __name__ == "__main__":
    init(autoreset=True)
    ensure_created_file()
    task_list = init_task_list()
    print("\n------------TODO LIST------------\n")
    print("To exit, enter q or control-C")
    while True:
        try:
            line = get_line()

            if line[0].strip().lower() == 'q':
                raise e.TerminateProgramException

            action = val_action(line[0].strip().lower())

            if len(line) == 1 and action != 'purge':
                line = cmd.cmd_prompt(action)

            val_line_format(line[1:])

            if action == "add":
                add_task(line[1:])
            elif action == "list":
                val_list_type(line[1:])
                print_header()
                if line[1].strip().lower() == 'all':
                    print_all()
                elif line[1].strip().lower() == 'todo':
                    print_todo()
            elif action == 'done':
                change_completion_status(line[1])
            elif action == 'rem':
                rem_task(line[1])
            elif action == 'upd':
                upd_task(line[1], line[2:])
            elif action == "purge":
                purge_task_list()

            if len(sys.argv) > 1:
                raise e.TerminateProgramException

        except (e.InvalidActionException, e.InvalidListTypeException, e.InvalidInputException) as msg:
            print(f'{Fore.RED}{msg}')
            if len(sys.argv) > 1:
                break

        except (KeyboardInterrupt, e.TerminateProgramException):
            write_to_file()
            print("\nExiting to-do App...")
            break
