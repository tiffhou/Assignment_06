#------------------------------------------#
# Title: Assignment06_Starter.py
# Desc: Working with classes and functions.
# Change Log: (Who, When, What)
# DBiesinger, 2030-Jan-01, Created File
# THou, 2020-Feb-27, added try statement to check for existing save file; added functions for adding entry, deleting entry; updated display
# THou, 2020-Feb-29, added auto-generating ID for new CD entries; cleaned up formatting
# THou, 2020-Mar-02, added more formatting and comments; tweaked naming conventions; added get_int_input()
#------------------------------------------#

# -- DATA -- #
strChoice = '' # User input
lstTbl = []  # list of lists to hold data
dicRow = {}  # list of data row
strFileName = 'CDInventory.txt'  # data storage file
objFile = None  # file object
intID = '' #variable to hold a CD ID
strTitle = '' #variable to hold a CD title
strArtist = '' #variable to hold a CD's artist

# -- PROCESSING -- #
class DataProcessor:
    """processess data in memory"""

    @staticmethod
    def add_entry(intID, strTitle, strArtist):
        """Adds the CD entry to a dictionary and appends it to the lstTbl.
        
        Args:
            intID (int): CD ID to be added to the dictionary
            strTitle (str): CD title to be added to the dictionary
            strArtist (string): CD artist to be added to the dictionary
            
        Return:
            none
        """
        dicRow = {'ID': intID, 'Title': strTitle, 'Artist': strArtist}
        lstTbl.append(dicRow)
        IO.show_inventory(lstTbl)

    @staticmethod
    def delete_entry(intIDDel):
        """Deletes a CD entry based on inputted ID (intIDDel).
        
        Args:
            delID (int): the ID inputted by the user for the entry to be deleted
        
        Return:
            None
        """
        intRowNr = -1
        blnCDRemoved = False
        for row in lstTbl:
            intRowNr += 1
            if row['ID'] == intIDDel:
                del lstTbl[intRowNr]
                blnCDRemoved = True
                break
        if blnCDRemoved:
            print('The CD was removed.\n')
        else:
            print('Could not find this CD!\n')
        IO.show_inventory(lstTbl)

    @staticmethod
    def generate_id():
        """Generates a CD ID based on lstTbl length. Checks for and increments until CD ID is a unique value.
        
        Args:
            None
        
        Returns:
            cdID (int): the auto-generated CD ID
        """
        cdID = '' #local variable for generating CD ID
        lenTable = len(lstTbl)
        if lenTable == 0:
            cdID = 1
        else:
            cdID = lenTable + 1
            while any(cdID == row['ID'] for row in lstTbl):
                cdID = cdID + 1
        return cdID

    @staticmethod
    def get_int_input(valInput):
        """Attempts to cast the inputted value as an integer.
        
        Args:
            None
        
        Returns:
            intInput (int): the input cast as an integer; otherwise returns None.
        """
        try:
            intInput = int(valInput)
            return intInput
        except:
            print ('Invalid entry. Returning to menu.')
            return None


class FileProcessor:
    """Processing the data to and from text file"""

    @staticmethod
    def read_file(file_name, table):
        """Function to manage data ingestion from file to a list of dictionaries
        
        Reads the data from file identified by file_name into a 2D table
        (list of dicts) table one line in the file represents one dictionary row in table.
        
        Args:
            file_name (string): name of file used to read the data from
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime
        
        Returns:
            None.
        """
        table.clear()  # this clears existing data and allows to load data from file
        objFile = open(file_name, 'r')
        for line in objFile:
            data = line.strip().split(',')
            dicRow = {'ID': int(data[0]), 'Title': data[1], 'Artist': data[2]}
            table.append(dicRow)
        objFile.close()

    @staticmethod
    def write_file(file_name, table):
        """Write the lstTbl in inventory to the text file.
        
        Args:
            None
        
        Returns:
            None
        """
        try:
            objFile = open(file_name, 'w')
            for row in table:
                lstValues = list(row.values())
                lstValues[0] = str(lstValues[0])
                objFile.write(','.join(lstValues) + '\n')
            objFile.close()
        except:
            print('The save attempt was not successful')


# -- PRESENTATION (Input/Output) -- #
class IO:
    """Handling Input / Output"""

    @staticmethod
    def print_menu():
        """Displays a menu of choices to the user
        
        Args:
            None.
        
        Returns:
            None.
        """
        print('\n\n[[ Menu ]]\n\n[l] load Inventory from file\n[a] Add CD\n[i] Display Current Inventory')
        print('[d] delete CD from Inventory\n[s] Save Inventory to file\n[x] exit\n')

    @staticmethod
    def menu_choice():
        """Gets user input for menu selection.
        
        Args:
            None.
            
        Returns:
            choice (string): a lower case sting of the users input out of the choices l, a, i, d, s or x
        """
        choice = ' '
        while choice not in ['l', 'a', 'i', 'd', 's', 'x']:
            choice = input('Which operation would you like to perform? [l, a, i, d, s or x]: ').lower().strip()
        print()  # Add extra space for layout
        return choice

    @staticmethod
    def show_inventory(table):
        """Displays current inventory table.
        
        Args:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime.
        
        Returns:
            None.
        """
        print('======= The Current Inventory: =======')
        print('ID\tCD Title (by: Artist)\n')
        for row in table:
            print('{}\t{} (by: {})'.format(*row.values()))
        print('======================================')

    @staticmethod
    def input_cd():
        """Gets the CD entry fields (ID, Title, Artist). Calls generate_id() to get auto ID instead of user input.
        
        Args:
            None
            
        Returns:
            intID (int): cleaned and validated inputted ID for a CD
            strTitle (str): cleaned inputted CD title
            strArtist (string): cleaned inputted CD artist
        """
        intID = DataProcessor.generate_id() #call generate_ID() to get ID
        print('CD ID: ', intID)
        strTitle = input('What is the CD\'s title? ').strip()
        strArtist = input('What is the Artist\'s name? ').strip()
        return intID, strTitle, strArtist


# -- MAIN BODY -- #
# 1. When program starts, read in the currently saved Inventory
try:
    FileProcessor.read_file(strFileName, lstTbl)
    print('\nCDInventory.txt loaded.')
    IO.show_inventory(lstTbl)
except FileNotFoundError:
    print('\nNo save file available. Loading menu.')
    pass


# 2. start main loop
while True:
    # 2.1 Display Menu to user and get choice
    IO.print_menu()
    strChoice = IO.menu_choice()


    # 3. Process menu selection
    # 3.1 process exit first
    if strChoice == 'x':
        break


    # 3.2 process load inventory
    if strChoice == 'l':
        print('WARNING: If you continue, all unsaved data will be lost and the Inventory re-loaded from file.')
        strYesNo = input('type \'yes\' to continue and reload from file. otherwise reload will be canceled')
        if strYesNo.lower() == 'yes':
            print('reloading...')
            FileProcessor.read_file(strFileName, lstTbl)
            IO.show_inventory(lstTbl)
        else:
            input('canceling... Inventory data NOT reloaded. Press [ENTER] to continue to the menu.')
            IO.show_inventory(lstTbl)
        continue  # start loop back at top.


    # 3.3 process add a CD
    elif strChoice == 'a':
        # 3.3.1 Ask user for new ID, CD Title and Artist
        intID, strTitle, strArtist = IO.input_cd()
        
        # 3.3.2 Add item to the table
        DataProcessor.add_entry(intID, strTitle, strArtist)
        continue  # start loop back at top.


    # 3.4 process display current inventory
    elif strChoice == 'i':
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.


    # 3.5 process delete a CD
    elif strChoice == 'd':
        # 3.5.1 get Userinput for which CD to delete
        # 3.5.1.1 display Inventory to user
        IO.show_inventory(lstTbl)
        # 3.5.1.2 ask user which ID to remove
        strID = input('Which ID would you like to delete? ').strip()
        intIDDel = DataProcessor.get_int_input(strID) #tries to cast as int
        
        # 3.5.2 search thru table and delete CD
        if intIDDel:
            DataProcessor.delete_entry(intIDDel)
        continue  # start loop back at top.


    # 3.6 process save inventory to file
    elif strChoice == 's':
        # 3.6.1 Display current inventory and ask user for confirmation to save
        IO.show_inventory(lstTbl)
        strYesNo = input('Save this inventory to file? [y/n] ').strip().lower()
        
        # 3.6.2 Process choice
        if strYesNo == 'y':
            # 3.6.2.1 save data
            FileProcessor.write_file(strFileName, lstTbl)
        else:
            input('The inventory was NOT saved to file. Press [ENTER] to return to the menu.')
        continue  # start loop back at top.


    # 3.7 catch-all should not be possible, as user choice gets vetted in IO, but to be save:
    else:
        print('General Error')