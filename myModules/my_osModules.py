import os

def single_object_check(target):
    '''
    PURPOSE:
        * Can do as os.path.exists
    '''
    if not os.path.isabs(target):
        return False
    if not os.path.exists(target):
        return False
    else:
        return True

# TODO
def multi_object_check(multi_target_list):
    '''
    PURPOSE:
        * Note whether multiple files or directories exists
        * Check existence of child files and folders with discover_file
    '''
    return False

def create_single_dir(target):
    '''
    PURPOSE:
        * Create a single directory
    '''
    if not os.path.isabs(target):
        print("Path must be absolute")
        return False
    while not os.path.exists(target):
            userInput_create_target = input(target + " directory does not exist, create(Y/N): ")
            if userInput_create_target.lower() == "y":
                try:
                    os.makedirs(target)
                except IOERROR:
                    print("Failed to create DIR, please check if you can create " + target + " manually")
                    return False
                return True
            elif userInput_create_target.lower() == "n":
                return False
            else:
                continue


def create_multi_dir(multi_target_list):
    return False
