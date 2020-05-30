def single_menuCreator(title, sub_title, contents):
    """
    PURPOSE:
        * print header
        * sequentially add a number for each additional entry
        * add content to each entry
        * returns the # associated with the index of the entry within the list given
        * if user quits, returns false
    IMPORT:
        from menuCreator import single_menuCreator
        while True:
            single_menuCreator('fake', 'sub_fake', [1,2,3]):
        ** once False is returned this while statement will then exit

    """
    ### GLOBAL VARIABLES ###
    try:
        num_of_entries = len(contents)
    except:
        print('contents is not a list type')

    ### Create our menu ###
    print( title + ' - ' + sub_title)
    print('{:=>20}'.format('='))
    counter=1
    # Loop through list given and create a menu option for it
    for content in contents:
        print(str(counter) + ')' + ' ' +  content)
        counter += 1
    print('q)' + ' Exit')

    ### User's gives a number assigned to the entry and that is returned ###
    while True:
        userinput_entry_select = input("# of your choice: ")
        if userinput_entry_select.lower() == 'q':
            return False
        # Validate user's input, must be an integer
        try:
            user_entry_as_int = int(userinput_entry_select)
        except:
            input('Invalid input...Press the <ENTER> key to continue...')
            continue
        if user_entry_as_int == 0 or user_entry_as_int > num_of_entries:
            input('Invalid input...Press the <ENTER> key to continue...')
            continue
        else:
            return user_entry_as_int
