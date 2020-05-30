#! /usr/bin/env python3

##########
# Name: Michael Zulian
# Last Update: 05/11/2018
# Purpose: Select a file type to convert from, script should grabs pieces of targeted plain text and then organize it in to a CSV format

import csv
import os
import re

####
# Function fileReader: User input for a file, validate that file and store its contents

def fileReader():
    while True:
        os.system('clear')
        pathToFile = input('Write out the full path to a file you want to do stuff to:\n\nWrite here: ')

        if os.path.exists(pathToFile):
            print('Will now proceed with conversion...')
            break
        else:
            print('The file does not exist, try again')
            os.system('sleep 2')
            os.system('clear')
            
    openFile = open(pathToFile)
    fileContent = openFile.read()

    os.system('clear')
    print(fileContent)
    input('Please scroll up and note file contents...Press ENTER to continue...')

    return fileContent


####
# Functions for different filetypes

# TODO: Add More file Types
# Function fileType VCF: Grab FIRSTNAME, EMAIL

def vcfFileType(fileContent):
    vcfNameRegex = re.compile(r'''
                                FN=(.*): #name
                                ([a-zA-Z0-9._%+-]+ # userName
                                @
                                [a-zA-Z0-9.-]+ # Domain
                                \.[a-zA-Z]{2,4}) # dot-something
                                ''', re.VERBOSE)
                                
    name = vcfNameRegex.findall(fileContent)

    firstNameAddCSV = []
    emailAddCSV = []
    for x,y in name:
            firstNameAddCSV.append(x)
            emailAddCSV.append(y)
    
    return firstNameAddCSV, emailAddCSV

####
# Function: Add to CSV, headers decided based off menu selection
# TODO: Add to CSV (how to check if file ends in .csv)

def csvDefined(vcfTargetName, vcfTargetEmail):#,menuSelection):
    while True:
        os.system('clear')
        csvFile = input('CSV file to create import into ThunderBird (ends in .csv):\n\nWrite here: ')
        
        try:
            outputCSVFile = open(csvFile, 'w', newline='')
        except (PermissionError, FileNotFoundError):
            print('The target destination either doesn\'t exist or you do not have permissions')
            os.system('sleep 2')
        
        if os.path.exists(csvFile):
            break
    fieldNames = ['First Name','Last Name','Display Name','Nickname','Primary Email','Secondary Email','Screen Name','Work Phone','Home Phone','Fax Number','Pager Number','Mobile Number','Home Address','Home Address 2','Home City','Home State','Home ZipCode','Home Country','Work Address','Work Address 2','Work City','Work State','Work ZipCode','Work Country','Job Title','Department','Organization','Web Page 1','Web Page 2','Birth Year','Birth Month','Birth Day','Custom 1','Custom 2','Custom 3','Custom 4','Notes'] 
    
    
    outputWriter = csv.DictWriter(outputCSVFile, fieldnames=fieldNames)
    outputWriter.writeheader()
    for name, email in zip(vcfTargetName, vcfTargetEmail):
        outputWriter.writerow({'First Name': name, 'Primary Email': email})
        
    outputCSVFile.close()                    
    
    
    
####
# CODE: Main menu
# TODO TWO: Select the source file type

fileContent = fileReader()
vcfTargetName, vcfTargetEmail = vcfFileType(fileContent)
csvDefined(vcfTargetName, vcfTargetEmail)




    
    
    
