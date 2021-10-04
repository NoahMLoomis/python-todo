import sys
import os
import exceptions as e


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
        self.completed = not self.completed

    def __str__(self):
        return f'{self.desc} {self.priority} {self.project}'
    
    def upd_desc(self, new_desc):
        self.desc = new_desc


def ensure_created_file():
    if not os.path.isfile('tasks.txt'):
        open('tasks.txt', 'w').close()


def get_new_task_id():
    if len(list(task_list)) < 1:
        return 1
    return int(list(task_list)[-1]) + 1


def get_task_id(task_id):
    if task_id in task_list:
        return task_id
    raise e.TaskNotFoundException(f'No task was found with task_id: {task_id}')


def get_priority(task):
    for word in task:
        if word[0] == '!':
            return word[1:]
    return None


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


def get_todo_sorted_by_priority():
    return sorted({key: task_list[key] for key in task_list if task_list[key].completed == 'False'}.items(), key=lambda s: s[1].priority)


def val_action(action):
    if action == "add" or action == "udp" or action == "rem" or action == "done" or action == "list" or action == "purge":
        return action
    raise e.InvalidActionException(
        "Invalid action. Action can be add, udp, rem, done, list or purge")


def val_list_type(list_type):
    if len(list_type) < 1 or list_type != "all" or list_type != "todo":
        raise e.InvalidListTypeException(
            "Can only list of type 'all' or 'todo'")


def print_header():
    print(
        f'\n{"Completed":^10}|{"Description":^45}|{"Priority":^15}|{"Project":^15}|')
    print("-----------------------------------------------------------------------------------------")


def print_all():
    for key in task_list:
        print(
            f'{task_list[key].completed:^10}|{task_list[key].desc:^45}|{task_list[key].priority:^15}|{task_list[key].project:^15}|')


def print_todo():
    for task in get_todo_sorted_by_priority():
        print(
            f'{task[1].completed:^10}|{task[1].desc:^45}|{task[1].priority:^15}|{task[1].project:^15}|')


def add_task(str):
    task_list[id] = Task(get_new_task_id(), get_desc(
        str), get_priority(str), get_project(str))


def rem_task(task_id):
    try:
        found_task_id = get_task_id(task_id)
        del task_list[found_task_id]
        print(f'Task removed with the task_id of {task_id}')
    except e.TaskNotFoundException as msg:
        print(msg)
        
def upd_task(task_id, new_desc):
    try:
        found_task_id = get_task_id(task_id)
        
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


def change_completion_status(task_id):
    try:
        found_task_id = get_task_id(task_id)
        task_list[found_task_id].change_completed()
    except e.TaskNotFoundException as msg:
        print(msg)


def prompt_add():
    print("Prompt for all the needed info")


if __name__ == "__main__":
    ensure_created_file()
    task_list = init_task_list()
    print("\n------------TODO LIST------------\n")
    while True:
        try:
            line = input("Please enter a command to start: ").split()
            action = val_action(line[0].strip()).lower()

            if action == "add":
                if len(line) > 1:
                    add_task(line[1:])
                else:
                    prompt_add()
            elif action == "list":
                val_list_type(line[1:])
                print_header()
                if line[1].strip().lower() == 'all':
                    print_all()
                elif line[1].strip().lower() == 'todo':
                    print_todo()
            elif action == 'done':
                if len(line) > 1:
                    change_completion_status(line[1])
            elif action == 'rem':
                rem_task(line[1])
            elif action == 'upd':
                upd_task(line[1], line[2:])

        except KeyboardInterrupt:
            write_to_file()
            print("\nExiting to-do list...")
            break
        except (e.InvalidActionException, e.InvalidListTypeException) as msg:
            print(msg)
