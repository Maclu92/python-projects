#! /usr/bin/env python3

"""
# Author: Michael Zulian
# Last Update: 05/28/2020
# Purpose --
    Various CSV Functions
# Details --
    1) Remove blank columns that have headers
    2) Compare a key-value pair to another key-value pair (think comparing # of \
        events for a month for whatever to another month)
    3) MORE TO COME

# General TODO -
    *
# Report Known Errors/Bugs -
    1)

"""

### Standard Library imports ###
import sys
import os
import csv

from datetime import date
from time import sleep
from menuCreator import single_menuCreator
from my_osModules import single_object_check
### Third-Party Imports (installed via pip) ###


### GLOBAL VARIABLES ###
cwd = os.getcwd()

### FUNCTIONS ###
def remove_blankColumns_withHeaders(target_csv, output_folder):
    '''
    PURPOSE:
        * Take in a CSV file and a destination folder
        * Rename the destination folder acknowledging change and date
        * Note columns that are completely blank, skipping headers 
    '''
    try:
        # Write all but the columns found to be blank
        columns_to_be_deleted = []
        columns_with_content = []
        # take off the file extension
        target_file_split = target_csv.split('/')
        renamed_output_file = output_folder + str(target_file_split[-1])[:-4] + '_blankHeadersRemoved_' + str(date.today()) + '.csv'
        # since its a file object, csv mod wants newline=''    
        with open(target_csv, 'r', newline='') as target_csv_read, \
            open(renamed_output_file, 'w', newline='') as target_csv_write:
            csv_reader = csv.reader(target_csv_read, delimiter=',')
            headers = next(csv_reader, None)
            csv_writer = csv.writer(target_csv_write, delimiter=',')
            # iterate over the all rows in the file to note columns with blanks
            for row in csv_reader:
                # iterate over the number of columns 
                for column in range(0,len(row)):
                    if row[column] == '':
                        # track the columns that are blank and haven't already been noted
                        if column not in columns_to_be_deleted and column not in columns_with_content:
                            columns_to_be_deleted.append(column)
                    # if a column is found to have contents remove it from the list
                    ## append that column number so that it isn't noted for deletion later on
                    elif column in columns_to_be_deleted :
                        columns_to_be_deleted.remove(column)
                        columns_with_content.append(column)
            for column in columns_to_be_deleted:
                print('Deleting the following columns: ' + headers[column] )
            # Reverse the list with the biggest # first to avoid index errors
            ## reading each row (indivdual list), starting at the back doesn't change the index of the ones before
            columns_to_be_deleted_rev = sorted(columns_to_be_deleted, reverse=True) 
            # reset the file read to write to the new file
            target_csv_read.seek(0)
            # Write output to new file
            for row in csv_reader:
                for column in columns_to_be_deleted_rev:
                        del row[column]
                csv_writer.writerow(row)
    except (PermissionError, FileNotFoundError):
        print('The target destination either doesn\'t exist or you do not have permissions')
        sleep(2)
# TODO
def compare_keyValue(target_csv):
    return False




### MAIN ###
def main():
    # User notes where the file is and where to save to
    while True:
        userInput_input_file = input('Please enter the ABSOLUTE path to the CSV file: ')
        if not single_object_check(userInput_input_file):
            print('Unable to access file, did you give an absolute path?')
            continue
        print('Destination file will have the same name as the original but appended with _modified_$date.csv.')
        userInput_output_folder = input("The ABSOLUTE path to where you\'d like the changed file to be saved (hit ..ENTER.. for cwd): )")
        if userInput_output_folder == '':
            userInput_output_folder == cwd
            break

    # Create the menu and launch functions
    csv_fucs = ['Remove blank columns with headers', 'Compare key-value pair with vlookups and arthimetic']
    fuc_selection = single_menuCreator('CSV PY Functions', 'Main Menu', csv_fucs )
    if fuc_selection == 1:
        remove_blankColumns_withHeaders(userInput_input_file, userInput_output_folder)
    elif fuc_selection == 2:
        compare_keyValue(userInput_input_file)

if __name__ == '__main__':
    main()
