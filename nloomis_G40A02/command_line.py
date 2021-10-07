import exceptions as e

def cmd_prompt_add():
    desc = input("Enter Description: ")
    if desc == "":
        raise e.InvalidInputException("You must enter a description")
    return_list = ['add', desc]

    priority = input("Enter Priority: ")
    project = input("Enter Project: ")
    if priority != "":
        return_list.append(f'!{priority}')
    if project != "":
        return_list.append(f'#{project}')

    return return_list


def cmd_prompt_done():
    task_id_to_change = input("Enter the task_id: ")
    return ['done', task_id_to_change]


def cmd_prompt_list():
    list_type = input("Please enter the type of list to display: ")
    return ['list', list_type]


def cmd_prompt_rem():
    task_id_to_change = input("Enter the task_id to remove: ")
    return ['rem', task_id_to_change]

def cmd_prompt_upd():
    task_id_to_change = input("Enter the task_id: ")
    desc = input("Enter the new description: ")
    if desc == "":
        raise e.InvalidInputException("You must enter a description")
    
    return_list = ['upd', task_id_to_change,  desc]
    priority = input("Enter the new Priority: ")
    project = input("Enter the new Project: ")
    
    if priority != "":
        return_list.append(f'!{priority}')
    if project != "":
        return_list.append(f'#{project}')
    return return_list

def cmd_prompt(action):
    if action == 'add':
        return cmd_prompt_add()
    elif action == "list":
        return cmd_prompt_list()
    elif action == "done":
        return cmd_prompt_done()
    elif action == 'rem':
        return cmd_prompt_rem()
    elif action == 'upd':
        return cmd_prompt_upd()