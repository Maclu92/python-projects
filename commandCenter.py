#! /usr/bin/env python3
"""
# Author: Michael Zulian
# Last Update: 02/21/2019
# Purpose --
    A simple menu allowing the user to choose from a list of useful commands that I've collected over time in the CLI
# Details --
    1) An infinite loop maintaining the menu with a tree-like structure of cmds (IE. Menu#1 - Pacman Menu#2 - UPDATE )
    2) Allow the user to add parameters to the cmds that require and also allow the option for a dry-run prior to each run if necessary for the cmd
    3) A simple method to add additional cmds without needing to continualy modify the menu
# General TODO -
# Report Known Errors/Bugs -
    1)
"""

### Standard Library imports ###
import subprocess
from time import sleep
from sys import exit
import pwd
import re
import csv
import os
import pdb
#from stat import *
import datetime


### VARIABLES ###
# Menu Content
mainMenu_title = "Main Menu"
mainMenu_exit = "Exit"
subMenu_exit = 'Back'
# Get user using the pwd module and checking if user is root
user = pwd.getpwuid(os.getuid()).pw_name
if user == "root":
    print("Please run as unprivileged user...")
    sleep(3)
    exit()
# Use that user's home bin folder
commandCenter_PWD = "/home/" + user + "/.commandCenterFiles/"
commandCenter_Files = commandCenter_PWD + "commandCenter_saved_commands.csv"


### FUNCTIONS ###
# CHECK: Existence of folder and/or file:
def file_or_folder_exist(target, file_or_dir, discover_file):
    '''
    PURPOSE:
        * Create the top folder
        * Use absolute paths and pass literal strings "file" or "dir" as a second arg, dependent on what the target is
        * Check existence of child files and folders with discover_file TODO
    '''
    if file_or_dir == "file" or file_or_dir == "dir":
        # Is path given absolute?
        if not os.path.isabs(target):
            print("Path must be absolute")
            exit()
        # Is target a directory?
        elif not os.path.exists(target) and file_or_dir == "dir":
            userInput_create_target = input(target + " directory does not exist, create(Y/N): ")
            if userInput_create_target.lower() == "y":
                try:
                    os.makedirs(target)
                except IOERROR:
                    print("Failed to create DIR, please check if you can create " + target + " manually")
                    exit()
                return True
            # Why is this a thing
            else:
                subprocess.run[("clear")]
                print('Whatever')
                sleep(2)
                exit()
        # Target must be a file
        elif not os.path.exists(target) and file_or_dir == "file":
            return False
        else:
            return True
    # Function not used correctly
    else:
        print('file_or_folder_exist - Function not used correctly')
        return False

# RETURNS: headers of CSV
def csv_column_header_handler(target,header):
    """
    PURPOSE:
        * file_or_folder_exist function checks for the existence, no need to double check here
        * returns headers, as this list is necessary for dynamic menu
    """
    headers = []
    with open(target, 'r') as csvfile:
        reader_dict = csv.DictReader(csvfile)
        headers = reader_dict.fieldnames
    return headers

# Takes in a fieldname and returns all values in that fieldname's column
def csv_column_row_handler(target, target_category):
    """
    PURPOSE:
        * return a list of rows within the specified column incase category == column
        * column choosen based off the header list returned by csv__column_header_handler
    """
    target_category_subMenu = []
    with open(target, 'r') as csvfile:
        reader_dict = csv.DictReader(csvfile)
        for row in reader_dict:
            target_category_subMenu.append(row[target_category])

    return filter(None,target_category_subMenu)

def csv_appender(target, user_input, target_category):
    '''
    PURPOSE(csv_appender):
        * Take an abs path to target CSV file
        * String of what to append to CSV file
        * Column name for where to append row
    >> It now does a backup, taking the file name and adding _backup_ along with datetime.datetime.now()
    >> Clean up old backups, TODO:
    '''

    # BACKUP OLD FILE
    target_file = os.path.basename(target) # just incase there's a '.' in the path name; as the below split would split on that
    backup_csv_file_split = target_file.split('.') # split file path (target) on "." meaning a list of 2, 2nd item being the file type
    backup_csv_file = os.path.dirname(target) + '/' + backup_csv_file_split[0] + '_backup_' + str(datetime.datetime.now().strftime('%Y_%m_%d')) + '.' + backup_csv_file_split[1] # Add _backup as well as date between filename and filetype


    os.system('cp ' + target + ' ' +  backup_csv_file)

    # GRAB A LIST OBJ CONTAINING TARGET COLUMN USING TARGET_CATEGORY AS INDEX
    target_category_subMenu = []
    with open(target, 'r+', newline='') as read_write_csvfile:
        reader_dict = csv.DictReader(read_write_csvfile)

        command_categories = reader_dict.fieldnames # Set header for the below dictwriter, as it requires fieldnames as a parameter
        writer_dict = csv.DictWriter(read_write_csvfile, fieldnames=command_categories, dialect="unix")

        for row in reader_dict:
            target_category_subMenu.append(row[target_category])

        # CLEAN UP BLANKS AND ADD NEW COMMAND
        clean_new_list = list(filter(None,target_category_subMenu)) # filter returns a filter obj, not a list hence the need for the manual conversion
        clean_new_list.append(user_input)

        # WRITE NEW LIST TO SPECIFIC COLUMN
        writer_dict.writerow({target_category: clean_new_list[-1]})


    # TODO: CLEAN UP BACKUPS
        # possible way with os to get parent folder
        # get_parent_dir_list = target.split('/')
        # get_parent_dir_list.pop(-1)
        # get_parent_dir = '/'.join(get_parent_dir_list)
    get_parent_dir = os.path.dirname(target)
    get_file_name = os.path.basename(target)
    get_parent_contents_list = os.listdir(get_parent_dir)

# Menu creation, accepts a title the menu's contents and an exit statement (quit|back)
def menuCreator(title, contents, exit_statement):
    """
    PURPOSE:
        * print header
        * dynamically create the menu based off the list of options given
        * some options must be permnant, like append/modify/delete
    """
    print('The Command Center - ' + title)
    print('{:=>20}'.format('='))
    counter=1
    # Loop through list given and create a menu option for it
    for content in contents:
        print(str(counter) + ')' + ' ' +  content)
        counter += 1
    # #1 manual option
    print(str(counter) + ')' + ' CONSTANT - Add more commands' )
    counter += 1 # Need to add to counter for each manual entry
    # #2 manual option
    print(str(counter) + ')' + ' CONSTANT - Modify Existing Commands' )
    counter += 1 # Need to add to counter for each manual entry
    print('q)' + ' ' + exit_statement)

# Maintaining the menu and saving user's choice of command and returning it a string
def menuMaintainer(mainMenu_content):
    """
    PURPOSE:
        * infinite while loop maintaining a while loop so menu is always present
        * execute other functions when user_input specifies so
    """
    # Main Menu infinite LOOP
    main_loop = 1
    while main_loop == 1:
        subprocess.run(["clear"])
        # Creates the menu
        menuCreator(mainMenu_title,mainMenu_content,mainMenu_exit)
        mainMenu_userInput=input('Enter Choice: ')

        if mainMenu_userInput == "q":
            subprocess.run(["clear"])
            print('Goodbye...')
            sleep(3)
            exit()

        # #CONSTANT #1: Add more commands. Check if user input is equal to one of the manual options
        if int(mainMenu_userInput) == int(len(mainMenu_content) + 1): # add or int(mainMenu_userInput) == int(len(mainMenu_content) + $WHATEVER_THE MANUAL OPTION) THIS IS PROBABLY GARBAGE WAY
            subprocess.run(["clear"])

            csv_appender_user_input_command=input('Press "q" to return to main menu :: Please type out the command as follows ($DESCRIPTION ($COMMAND)): ') # TODO: Regex to check against user input for correct formatting, maybe even possible testing

            if csv_appender_user_input_command.lower() == "q":
                continue

            while True:
                csv_appender_user_input_category=input('Which category does this command belong to? (type in "?" to list off available categories): ')



                if csv_appender_user_input_category == "?":
                    for category in mainMenu_content:
                        print(category)
                    continue

                if csv_appender_user_input_category not in mainMenu_content:
                    print('That is not a category, try again')
                    continue

                if csv_appender_user_input_category.lower() == "q":
                    continue

                # Execute csv_appender function with user_inputs
                csv_appender(commandCenter_Files, csv_appender_user_input_command, csv_appender_user_input_category)
                break
            continue

        # #CONSTANT #2: Modify the Excel sheet. Check if user input is equal to one of the manual options
        if int(mainMenu_userInput) == int(len(mainMenu_content) + 2): # add or int(mainMenu_userInput) == int(len(mainMenu_content) + $WHATEVER_THE MANUAL OPTION) THIS IS PROBABLY GARBAGE WAY
            subprocess.run(["clear"])

            csv_modifier_user_input_command=input('Press "q" to return to main menu :: Press ENTER to continue opening libreoffice')

            if csv_modifier_user_input_command.lower() == "q":
                continue

            subprocess.run(["libreoffice", "/home/maclu/.commandCenterFiles/commandCenter_saved_commands.csv"])
            continue
        # Need to minus users input by 1 to match list's index (Starts at 0), in a try block to check if possible to convert str to int
        try:
            choice_asListIndex = int(mainMenu_userInput) - 1
        except ValueError:
            subprocess.run(["clear"])
            print('Incorrect Input: ' + '1-' + str(len(mainMenu_content)) + ' or q are valid')
            sleep(2)
            continue

        # Check userInput against the number of actual options available
        if int(mainMenu_userInput) > len(mainMenu_content):
            subprocess.run(["clear"])
            print('Incorrect Input: ' + '1-' + str(len(mainMenu_content)) + ' or q are valid')
            sleep(2)
            continue



        """
        SubMenu LOOP
                * Call menuCreator function giving it the main menu selection, using the title of the submenu from the list of the main menu and populating the result from a dictionary with numeric keys which are mapped to whichever number the user chose.
                * Using re module to grab the cmd that should be written inside parenthesises and assess it for additional userInput or checks
        """
        while True:
            subprocess.run(["clear"])
            # Function will grab content of row associated with field choosen in the mainMenu content
            mainMenu_user_choice_subMenu_values_nonList = csv_column_row_handler(commandCenter_Files, mainMenu_content[choice_asListIndex])
            mainMenu_user_choice_subMenu_values = list(mainMenu_user_choice_subMenu_values_nonList)

            menuCreator(mainMenu_content[choice_asListIndex],mainMenu_user_choice_subMenu_values,subMenu_exit)
            # The key in the key-value pair matching the user's choice in the main menu to a submenu's contents, the value being a list which will then populate the submenu
            #            list_of_subMenu_userInput = subMenu_contents[str(mainMenu_userInput)]
            subMenu_userInput = input('Enter Choice: ')

            if subMenu_userInput == "q":
                break

            # Need to minus users input by 1 to match list's index (Starts at 0), in a try block to check if possible to convert str to int
            try:
                subChoice_asListIndex = int(subMenu_userInput) - 1
            except ValueError:
                subprocess.run(["clear"])
                print('Incorrect Input: ' + '1-' + str(len(list(mainMenu_user_choice_subMenu_values))) + ' or q are valid')
                sleep(2)
                continue

            # Check userInput against the number of actual options available
            if int(subMenu_userInput) > len(mainMenu_user_choice_subMenu_values):
                subprocess.run(["clear"])
                print('Incorrect Input, note ' + '1-' + str(len(list(mainMenu_user_choice_subMenu_values))) + ' or q, are valid')
                sleep(2)
                continue

            else:
                # Break out of  the ENTIRE while loop (interactive menu) and launch into the cmd at the cmdline
                cmdChosen = mainMenu_user_choice_subMenu_values[int(subChoice_asListIndex)]
                main_loop = 0
                return cmdChosen
                break

# Regex and command execution, accepts string variable, format $DESCRIPTION ($CMD)
def menuExecutor(cmdChosen):
    # We now have a list of cmds the user can choose from, each with a description and a cmd in parenthesises, using the following regex we can grab the cmd
    command_regex = re.compile(r'\((.+)\)')
    command_search= command_regex.search(cmdChosen)
    command = command_search.group(1)

    # We now have the cmd as a string, we now to deem whether it requires further userInput or preleminary tests such as a backup of a file or to run a --dry-run or producing a list of forums with reponses to recent updates or changelogs of that update prior to a system or app update.
    command_userCheck = input("This is the command you're about to run command:\n\n" + command +  "\n\nAre you certain? (Y/N): ")
    if command_userCheck.lower() == "y":
        if "$userInput" not in str(command):
            pass
        else:
            while True:
                command_userInput = input("What would you like to do with this command (will change out first $userInput): ..." + str(command) + "... ENTER HERE: ")
                command = command.replace('$userInput', command_userInput)
                command_userCheck = input("This is the command you're about to run command:\n\n" + command +  "\n\nAre you certain? (Y/N): ")
                if command_userCheck.lower() == "y":
                    break
                else:
                    continue
        if command.endswith(('.sh', '.py')):
            subprocess.call(f"{command}", shell=True)
        else:
            subprocess.run([f"{command}"], shell=True)
            #subprocess.run(["{}".format(command)], shell=True)
    else:
        cmdChosen = main()
        menuExecutor(cmdChosen)

def main():
    # Run against file_or_folder_exist function to check for permissions and exsitence
    if file_or_folder_exist(commandCenter_PWD,"dir",0):
        # Grab a list of the headers of the CSV
        favCommandsCSV_headers = csv_column_header_handler(commandCenter_Files, "csv")
        # Execute the interactive menu and return the specfic cell value which should be of the cmd
        command_chosen = menuMaintainer(favCommandsCSV_headers)
        # Execute that command
        menuExecutor(command_chosen)
    else:
        print("Check the following target for permission and/or existence issues: " + commandCenter_PWD)

### MAIN ###
if __name__ == '__main__':

    main()
