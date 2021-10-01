import sys

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


def get_new_task_id():
    if len(list(task_list)) < 1:
        return 1
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
    task_list[id] = Task(get_new_task_id(), get_desc(str), get_priority(str), get_project(str))


def get_task_id(task_str):
    return int(task_str[0])


def print_all():
    print(f'\n{"Completed":^10}|{"Description":^45}|{"Priority":^15}|{"Project":^15}|\n')
    print("-----------------------------------------------------------------------------------------")
    for key in task_list:
        print(f'{task_list[key].completed:^10}|{task_list[key].desc:^45}|{task_list[key].priority:^15}|{task_list[key].project:^15}|')

def print_todo():
    for key in task_list:
        print(task_list[key])

def write_to_file():
    out_file = open('tasks.txt', 'w')
    for key in task_list:
        out_str = task_list.get(key).get_write_string()
        if list(task_list)[-1] == key:
            out_file.write('\n' + out_str)
        else:
            out_file.write(out_str)


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

def change_completion_status(task_num_to_update):
    found_task = task_list[task_num_to_update]
    found_task.change_completed()



def prompt_add():
    print("Prompt for all the needed info")

if __name__ == "__main__":
    task_list = init_task_list()
    print("""
          ------------TODO LIST------------
          """)
    while True:
        line = input("Please enter a command to start: ").split()
        action = val_action(line[0].strip()).lower()
        if action == "add":
            if len(line) > 1:
                add_to_list(line[1:])
            else:
                prompt_add()
        elif action == "list":
            if line[1].strip().lower() == 'all':
                print_all()
            elif line[1].strip().lower() == 'todo':
                print_todo()
            else:
                raise Exception("Can only list of type 'all' or 'todo'")
        elif action == 'done':
            if len(line) > 1:
                change_completion_status(line[1])
                break
    write_to_file()