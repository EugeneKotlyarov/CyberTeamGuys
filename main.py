# Local project imports
from modules import const                    # Constants used in the program
from modules.errors import input_error       # Custom error handling for user input

from classes.record import Record            # Class for handling individual contact records
from classes.addressbook import AddressBook  # Class for handling the address book

# Global imports
import pickle                                # For serialization of data
import os                                    # For operating system dependent functionality
import platform                              # To check the operating system type

from colorama import Style                   # For colored terminal output
from subprocess import call                  # For running system commands

from classes.notebook import NoteBook        # Class for handling notes

# Command menu for the assistant bot
COMMANDS_MENU = f"""
Assistant bot's commands menu:
- contact -
 card-add <name> <number> \t\t# add contact with number to phone book
 card-add-phone <name> <number> \t# add number to contact
 card-edit <name> <old_num> <new_num> \t# change contact's number
 card-find <name> \t\t\t# show contact's card by its name (if exist)
 card-delete <name> \t\t\t# delete all contact info
 card-show-all\t\t\t\t# show all contacts in the book
- emails -
 email-add <name> <date> \t\t# add contact's email
 email-show <name>\t\t\t# show contact's email 
- birthdays -
 birthday-add <name> <date> \t\t# add contact's birthday
 birthday-show <name>\t\t\t# show contact's birthday
 birthday-in <N>\t\t\t# show birthdays next N days
- notes -
 note-add\t\t\t\t# add note step-by-step
 note-show-all\t\t\t\t# show all notes
 note-edit <id> <new_text>\t\t# edit note by id
 note-delete <id>\t\t\t# delete note by id
- leave - 
 exit | close \t\t\t\t# exit from assistant
"""

# ===== Parse user input into command and parameters =====
def parse_input(user_input):
    cmd, *args = user_input.split()  # Split the input into command and arguments
    cmd = cmd.strip().lower()        # Normalize the command (lowercase and stripped of whitespace)
    return cmd, *args                # Return command and arguments

# ===== BLOCK FOR CALLING FUNCTIONS FROM MAIN ===== START

@input_error  # Decorator for error handling
def card_add(args, book: AddressBook):
    name, phone, *_ = args                              # Extract name and phone from arguments
    record = Record(name)                               # Create a new Record object
    record.phone_add(phone)                             # Add the phone number to the record
    book.add_record(record)                             # Add the record to the address book
    print(f"{const.COLOR_DONE}New contact card added")  # Confirmation message

@input_error
def card_add_phone(args, book: AddressBook):
    name, phone, *_ = args                              # Extract name and phone from arguments
    record = book.find(name)                            # Find the record by name
    record.phone_add(phone)                             # Add the new phone number
    print(f"{const.COLOR_DONE}Phone added")             # Confirmation message

@input_error
def card_edit(args, book: AddressBook):
    name, old_phone, new_phone, *_ = args               # Extract necessary arguments
    record = book.find(name)                            # Find the record by name
    record.edit_phone(old_phone, new_phone)             # Edit the phone number
    print(f"{const.COLOR_DONE}Phone changed")           # Confirmation message

@input_error
def card_find(args, book: AddressBook):
    name, *_ = args                                     # Extract the name argument
    record = book.find(name)                            # Find the record
    print(record)                                       # Print the contact's information

@input_error
def card_delete(args, book: AddressBook):
    name, *_ = args                                     # Extract the name argument
    record = book.delete(name)                          # Delete the record

@input_error
def all(book: AddressBook):
    book.all()                                          # Show all contacts in the address book

@input_error
def email_add(args, book: AddressBook):
    name, email, *_ = args                              # Extract name and email
    record = book.find(name)                            # Find the record by name
    record.email_add(email)                             # Add the email to the record
    print(f"{const.COLOR_DONE}E-mail added")            # Confirmation message

@input_error
def birthday_add(args, book: AddressBook):
    name, birthday, *_ = args                           # Extract name and birthday
    record = book.find(name)                            # Find the record by name
    record.birthday_add(birthday)                       # Add the birthday to the record
    print(f"{const.COLOR_DONE}Birthday added")          # Confirmation message

@input_error
def birthday_show(args, book: AddressBook):
    name, *_ = args                                                         # Extract the name argument
    record = book.find(name)                                                # Find the record
    if record.birthday is None:                                             # Check if birthday is set
        print(f"{const.COLOR_ERROR}{name}'s birthday date does not set")    # Error message
    else:
        print(f"{const.COLOR_DONE}{name}'s birthday is {record.birthday}")  # Show birthday

@input_error
def birthday_in(args, book: AddressBook):
    days, *_ = args                                     # Extract the number of days
    book.get_upcoming_birthdays(int(days))              # Show upcoming birthdays

@input_error
def add_note(notebook: NoteBook):
    ID = notebook.add_note()                                # Add a note and get its ID
    print(f"{const.COLOR_DONE}Note added with ID: {ID}")    # Confirmation message

@input_error
def note_delete(args, notebook: NoteBook):
    note_id, *_ = args                                  # Extract the note ID
    notebook.delete_note(note_id)                       # Delete the note
    print(f"{const.COLOR_DONE}Note deleted")            # Confirmation message

@input_error
def note_edit(args, notebook: NoteBook):
    note_id = args[0]                                       # Extract the note ID
    new_text = " ".join(args[1:])                           # Combine the rest of the arguments into new text
    notebook.edit_note(note_id, new_text)                   # Edit the note
    print(f"{const.COLOR_DONE}Note updated successfully")   # Confirmation message

@input_error
def note_show_all(notebook: NoteBook):
    notebook.show_all_notes()                           # Show all notes

# ===== BLOCK FOR CALLING FUNCTIONS FROM MAIN ===== END

# ===== BLOCK FOR SAVE AND RESTORE DATA ===== START

@input_error
def save_data(book: AddressBook, filename="addressbook.pkl"):
    with open(filename, "wb") as f:                     # Open file to write binary data
        pickle.dump(book, f)                            # Serialize and save the address book

@input_error
def save_data_note(notebook: NoteBook, filename="notebook.pkl"):
    with open(filename, "wb") as f:                     # Open file to write binary data
        pickle.dump(notebook, f)                        # Serialize and save the notebook

@input_error
def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:                                                 # Try to open the file for reading
            print(f"{const.COLOR_DONE}Local address book was found and loaded")         # Success message
            return pickle.load(f)                                                       # Deserialize and return the address book
    except FileNotFoundError:
        print(f"{const.COLOR_ERROR}Local address book was NOT found. Empty created")    # Error message
        return AddressBook()                                                            # Return a new empty address book

@input_error
def load_data_note(filename="notebook.pkl"):
    try:
        with open(filename, "rb") as f:                                             # Try to open the file for reading
            print(f"{const.COLOR_DONE}Local note book was found and loaded")        # Success message
            return pickle.load(f)                                                   # Deserialize and return the notebook
    except FileNotFoundError:
        print(f"{const.COLOR_ERROR}Local note book was NOT found. Empty created")   # Error message
        return NoteBook()                                                           # Return a new empty notebook

# ===== BLOCK FOR SAVE AND RESTORE DATA ===== END

# Check the operating system and clear the console accordingly
def clear():
    os.system("cls" if platform.system() == "Windows" else "clear")

# ===== MAIN ===== START
def main():
    clear()                                      # Clear the console
    book = load_data()                           # Load or create a new address book
    notebook = load_data_note()                  # Load or create a new notebook
    print(f"{const.COLOR_MENU}{COMMANDS_MENU}")  # Display the command menu

    while True:
        user_input = input(f"{const.COLOR_MENU}Enter a command ('menu' for menu): ")    # Prompt for user input
        command, *args = parse_input(user_input)                                        # Parse the input
        clear()  # Clear the console

        if command in ["close", "exit"]:                # Check for exit commands
            print(f"{const.COLOR_DONE}\nGood bye!")     # Farewell message
            save_data(book)                             # Save the address book
            save_data_note(notebook)                    # Save the notebook
            break                                       # Exit the loop

        # Command handling for various actions
        elif command == "card-add":
            print(f"{const.COLOR_MENU}{COMMANDS_MENU}")
            card_add(args, book)

        elif command == "card-add-phone":
            print(f"{const.COLOR_MENU}{COMMANDS_MENU}")
            card_add_phone(args, book)

        elif command == "card-edit":
            print(f"{const.COLOR_MENU}{COMMANDS_MENU}")
            card_edit(args, book)

        elif command == "card-find":
            print(f"{const.COLOR_MENU}{COMMANDS_MENU}")
            card_find(args, book)

        elif command == "card-delete":
            print(f"{const.COLOR_MENU}{COMMANDS_MENU}")
            card_delete(args, book)

        elif command == "card-show-all":
            print(f"{const.COLOR_MENU}{COMMANDS_MENU}")
            all(book)

        elif command == "email-add":
            print(f"{const.COLOR_MENU}{COMMANDS_MENU}")
            email_add(args, book)

        elif command == "birthday-add":
            print(f"{const.COLOR_MENU}{COMMANDS_MENU}")
            birthday_add(args, book)

        elif command == "birthday-show":
            print(f"{const.COLOR_MENU}{COMMANDS_MENU}")
            birthday_show(args, book)

        elif command == "birthday-in":
            print(f"{const.COLOR_MENU}{COMMANDS_MENU}")
            birthday_in(args, book)

        elif command == "note-add":
            print(f"{const.COLOR_MENU}{COMMANDS_MENU}")
            add_note(notebook)

        elif command == "note-show-all":
            print(f"{const.COLOR_MENU}{COMMANDS_MENU}")
            note_show_all(notebook)

        elif command == "note-edit":
            print(f"{const.COLOR_MENU}{COMMANDS_MENU}")
            note_edit(args, notebook)

        elif command == "note-delete":
            print(f"{const.COLOR_MENU}{COMMANDS_MENU}")
            note_delete(args, notebook)

        else:
            print(f"{const.COLOR_MENU}{COMMANDS_MENU}")
            print(f"{const.COLOR_ERROR}Invalid command")    # Error message for invalid commands

# ===== MAIN ===== END

# ===== ENTRANCE POINT =====
if __name__ == "__main__":
    main()                      # Run the main function