#! /usr/bin/env python3

# Author: Michael Zulian
# Last Update: 01/03/2019
# Purpose --
"""
    A simple menu allowing the user to choose from a list of useful commands that I've collected over time in the CLI
# Details --
    1) An infinite loop maintaining the menu with a tree-like structure of cmds (IE. Menu#1 - Pacman - BACKUP - IPTABLES )
    2) Allow the user to modify the cmd, also allow the option for a dry-run prior to each run
    3) A simple method to add additional cmds without needing to continualy modify the menu
# General TODO -
    1)
# Report Known Errors/Bugs -
    1)
"""

### MODULES ###
from os import system
from time import sleep
from sys import exit
import re

### VARIABLES ###

mainMenu_title = "Main Menu"
mainMenu_content = ["Package Management",
                    "Networking",
                    "Storage",
                    "Hardware",
                    "BACKUPs",
                    "Useful MISC CMDs"]
mainMenu_exit = "Exit"

subMenu_contents = {
                    '1' : ["Update System (pacman -Syu)",
                            "Query Installed pkgs (pacman -Q | grep $userInput)" ],
                    '2' : ["WoL (/home/maclu/Projects/homeNetwork/scripts/WoL.sh)",
                            "Last 10 dropped packets ()"],
                    '3' : ["Largest folder->file (ncdu)",
                           ""]


                    }
subMenu_exit = 'Back'

"""
 TODO:
        * We now have dynamic menus and submenus, now need to map the options in the submenus to actual cmds, HOW
        * Create actual variables
"""

### FUNCTIONS ###
def menuCreator(title, contents, exit_statement):
    print('The Command Center - ' + title)
    print('{:=>20}'.format('='))
    counter=1
    for content in contents:
        print(str(counter) + ')' + ' ' +  content)
        counter += 1
    print('q)' + ' ' + exit_statement)


### MAIN ###
if __name__ == '__main__':
    # Main Menu LOOP
    while True:
        system('clear')
        menuCreator(mainMenu_title,mainMenu_content,mainMenu_exit)
        mainMenu_userInput=input('Enter Choice: ').lower()

        if mainMenu_userInput == "q":
            system('clear')
            print('Goodbye...')
            sleep(3)
            exit()

        elif int(mainMenu_userInput) > len(mainMenu_content):
            system('clear')
            print('Incorrect Input, note ' + '1-' + str(len(mainMenu_content)) + ' or q, are valid')
            sleep(2)
            continue

        try:
            choice_asListIndex = int(mainMenu_userInput) - 1
        except ValueError:
            system('clear')
            print('Incorrect Input' + '1-' + str(len(mainMenu_content)) + ' or q, are valid')
            sleep(2)
            continue
        """
        SubMenu LOOP
                * Call menuCreator function giving it the main menu selection
        while True:
            system('clear')
            menuCreator(mainMenu_content[choice_asListIndex],subMenu_contents[str(mainMenu_userInput)],subMenu_exit)
            list_of_subMenu_userInput = subMenu_contents[str(mainMenu_userInput)]
            subMenu_userInput = input('Enter Choice: ').lower()

            if subMenu_userInput == "q":
                break

            elif int(subMenu_userInput) > len(list_of_subMenu_userInput):
                system('clear')
                print('Incorrect Input, note ' + '1-' + str(len(list_of_subMenu_userInput)) + ' or q, are valid')
                sleep(2)
                continue

            else:
                subChoice_asListIndex = int(subMenu_userInput) - 1
                command_regex = re.compile(r'\((.+)\)')
                command = command_regex.search(list_of_subMenu_userInput[int(subChoice_asListIndex)])

                if "userInput" not in str(command.group(1)):
                    system(command.group(1))
                else:
                    command_userInput = input("What would you like to do with this command: ..." + str(command.group(1)) + "... ENTER HERE: ")




