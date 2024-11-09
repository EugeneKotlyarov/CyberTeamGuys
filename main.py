# local project import

from modules import const
from modules.errors import input_error

from classes.record import Record
from classes.addressbook import AddressBook

# global import

import pickle
import os
import platform

from colorama import Style
from subprocess import call

from classes.record import Record
from classes.addressbook import AddressBook
from classes.notebook import NoteBook

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


# ===== parse user input into command and parameters
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@input_error
def card_add(args, book: AddressBook):
    name, phone, *_ = args
    record = Record(name)
    record.phone_add(phone)
    book.add_record(record)
    print(f"{const.COLOR_DONE}New contact card added")


@input_error
def card_add_phone(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    record.phone_add(phone)
    print(f"{const.COLOR_DONE}Phone added")


@input_error
def card_edit(args, book: AddressBook):
    name, old_phone, new_phone, *_ = args
    record = book.find(name)
    record.edit_phone(old_phone, new_phone)
    print(f"{const.COLOR_DONE}Phone changed")


@input_error
def card_find(args, book: AddressBook):
    name, *_ = args
    record = book.find(name)
    print(record)


@input_error
def card_delete(args, book: AddressBook):
    name, *_ = args
    record = book.delete(name)


@input_error
def all(book: AddressBook):
    book.all()


@input_error
def email_add(args, book: AddressBook):
    name, email, *_ = args
    record = book.find(name)
    record.email_add(email)
    print(f"{const.COLOR_DONE}E-mail added")


@input_error
def birthday_add(args, book: AddressBook):
    name, birthday, *_ = args
    record = book.find(name)
    record.birthday_add(birthday)
    print(f"{const.COLOR_DONE}Birthday added")


@input_error
def birthday_show(args, book: AddressBook):
    name, *_ = args
    record = book.find(name)
    if record.birthday == None:
        print(f"{const.COLOR_ERROR}{name}'s birthday date does not set")
    else:
        print(f"{const.COLOR_DONE}{name}'s birthday is {record.birthday}")


@input_error
def birthday_in(args, book: AddressBook):
    days, *_ = args
    book.get_upcoming_birthdays(int(days))


@input_error
def add_note(notebook: NoteBook):
    ID = notebook.add_note()
    print(f"{const.COLOR_DONE}Note added with ID: {ID}")


@input_error
def note_delete(args, notebook: NoteBook):
    note_id, *_ = args
    notebook.delete_note(note_id)
    print(f"{const.COLOR_DONE}Note deleted")


@input_error
def note_edit(args, notebook: NoteBook):
    note_id = args[0]
    new_text = " ".join(args[1:])
    notebook.edit_note(note_id, new_text)
    print(f"{const.COLOR_DONE}Note updated successully")


@input_error
def note_show_all(notebook: NoteBook):
    notebook.show_all_notes()


@input_error
def save_data(book: AddressBook, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)


@input_error
def save_data_note(notebook: NoteBook, filename="notebook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(notebook, f)


@input_error
def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            print(f"{const.COLOR_DONE}Local address book was found and loaded")
            return pickle.load(f)
    except FileNotFoundError:
        print(f"{const.COLOR_ERROR}Local address book was NOT found. Empty created")
        return AddressBook()


@input_error
def load_data_note(filename="notebook.pkl"):
    try:
        with open(filename, "rb") as f:
            print(f"{const.COLOR_DONE}Local note book was found and loaded")
            return pickle.load(f)
    except FileNotFoundError:
        print(f"{const.COLOR_ERROR}Local note book was NOT found. Empty created")
        return NoteBook()


def clear():
    # check and make call for specific operating system
    os.system("cls" if platform.system() == "Windows" else "clear")


def main():
    clear()
    # Створення нової адресної книги або через відновлення
    book = load_data()
    # Створення нового записника або через відновлення
    notebook = load_data_note()
    print(f"{const.COLOR_MENU}{COMMANDS_MENU}")

    while True:
        user_input = input(f"{const.COLOR_MENU}Enter a command ('menu' for menu): ")
        command, *args = parse_input(user_input)
        clear()

        if command in ["close", "exit"]:
            print(f"{const.COLOR_DONE}\nGood bye!")
            save_data(book)
            save_data_note(notebook)
            break

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
            print(f"{const.COLOR_ERROR}Invalid command")


if __name__ == "__main__":
    main()
