import sys
import random as rand

task_list = {}


class Task():
    def __init__(self, task_id, desc, priority=None, project=None, action=None, completed=False):
        self.desc = desc
        self.priority = priority
        self.project = project
        self.task_id = task_id
        self.action = action
        self.completed = completed

    def get_write_string(self):
        return f'{self.task_id}~{self.desc}~{self.completed}~{self.priority}~{self.project}'

    def __str__(self):
        return f'{self.desc} {self.priority} {self.project}'


def get_new_task_id():
    return int(list(task_list)[-1]) + 1


def val_action(action):
    if action == "add" or action == "udp" or action == "rem" or action == "done" or action == "list" or action == "purge":
        return action
    raise Exception("Bad action, must be add, udp, rem, done, list or purge")


def get_priority(task):
    for word in task:
        if word[0] == '!':
            return word
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
            return word
    return None


def add_to_list(str):
    priority = get_priority(str)
    project = get_project(str)
    desc = get_desc(str)
    id = get_new_task_id()
    task_list[id] = Task(id, desc, priority, project)


def get_task_id(task_str):
    return task_str[0]


def print_list():
    print(task_list)


def write_to_file():
    print(task_list)
    open('tasks.txt', 'w').close()
    out_file = open('tasks.txt', 'a')
    for task in task_list:
        print(task_list.get(task))
        out_str = task_list.get(task).get_write_string()
        out_file.write(out_str)

def init_task_list():
    task_file = open('tasks.txt')
    tasks = {}
    for t in task_file.readlines():
        id = t.split("~")[0]
        desc = t.split("~")[1]
        priority = t.split("~")[3]
        project = t.split("~")[4]
        tasks[id] = Task(id, desc, priority, project)
    return tasks


if __name__ == "__main__":
    task_list = init_task_list()
    line = input("""
          TODO LIST
    Please enter a command      
          to start: """).split()
    action = val_action(line[0].strip())
    if action == "add":
        add_to_list(line[1:])
    elif action == "list":
        print_list()

    write_to_file()
