from classes.fields import Name, Phone, Birthday, Email
from classes.record import Record
from classes.addressbook import AddressBook

from modules import const
from modules.errors import input_error

import pickle
from prettytable import PrettyTable
import re
import sys


from colorama import Style
from datetime import datetime as dt
from datetime import timedelta as tdelta
from os import system, name
from subprocess import call

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
 note-add <text_note>\t\t\t# add note
 note-show-all\t\t\t\t# show all notes
 note-edit <id>\t\t\t\t# edit note by id
 note-delete <id>\t\t\t# delete note by id
- leave - 
 exit | close \t\t\t\t# exit from assistant
"""


# Validation for correct number made with own exception in class Phone
#
# all the classes has their methods with realisation and all works fine
#
# mainly prints copied from the task, added a couple other for better visualisation
# of result
# all
#
# class Birthday added with ValueError exception detection
#
# function ADD_BIRTHDAY added without checking for existing data, so each execution
# for existing contact will update his birthday date, i think it's OK
#
# __str__ function for class Record now print info with birthday
#
# class AddressBook now has a GET_UPCOMING_BIRTHDAYS function adopted from HW-03-04
# and re-mastered for classes structure.
# Return list of dicts with keys: 'name' and 'congratulation_date'. Tested, working GOOD
# BUT
# it is too long, so it's a good idea to export it an external file in future
#
# errors checks fixed/ Changed from "return" to "print" directly
# added realisation for save and load address book state with pickle
#


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@input_error
def card_add(args, book: AddressBook):
    name, phone, *_ = args
    record = Record(name)
    record.add_phone(phone)
    book.add_record(record)


@input_error
def card_add_phone(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    record.add_phone(phone)


@input_error
def card_edit(args, book: AddressBook):
    name, old_phone, new_phone, *_ = args
    record = book.find(name)
    record.edit_phone(old_phone, new_phone)


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


@input_error
def add_birthday(args, book: AddressBook):
    name, birthday, *_ = args
    record = book.find(name)
    record.add_birthday(birthday)


@input_error
def show_birthday(args, book: AddressBook):
    name, *_ = args
    record = book.find(name)
    if record.birthday == None:
        print(f"{name}'s birthday date does not set")
    else:
        print(f"{name}'s birthday is {record.birthday}")


@input_error
def birthdays(args, book: AddressBook):
    days, *_ = args
    for r in book.get_upcoming_birthdays(days):
        print(f"{const.COLOR_DONE}{r["name"]} = {r["congratulation_date"]}")


def save_data(book: AddressBook, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)


def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()


def clear():
    # check and make call for specific operating system
    _ = call("clear" if name == "posix" else "cls")


def main():
    clear()
    # Створення нової адресної книги або через відновлення
    book = load_data()
    print(f"{const.COLOR_MENU}{COMMANDS_MENU}")

    while True:
        user_input = input(f"{const.COLOR_MENU}Enter a command: ")
        command, *args = parse_input(user_input)
        clear()

        if command in ["close", "exit"]:
            print(f"{const.COLOR_DONE}\nGood bye!")
            save_data(book)
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
            add_birthday(args, book)

        elif command == "birthday-show":
            print(f"{const.COLOR_MENU}{COMMANDS_MENU}")
            show_birthday(args, book)

        elif command == "birthdays-in":
            print(f"{const.COLOR_MENU}{COMMANDS_MENU}")
            birthdays(book)

        elif command == "note-add":
            pass

        elif command == "note-show-all":
            pass

        elif command == "note-edit":
            pass

        elif command == "note-delete":
            pass

        else:
            print(f"{const.COLOR_MENU}{COMMANDS_MENU}")
            print(f"{const.COLOR_ERROR}Invalid command")


if __name__ == "__main__":
    main()
