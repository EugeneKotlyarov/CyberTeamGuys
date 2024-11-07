from modules import const
from modules.errors import input_error

import pickle
from prettytable import PrettyTable
import re
import sys

from collections import UserDict

from colorama import Style
from datetime import datetime as dt
from datetime import timedelta as tdelta
from os import system, name
from subprocess import call

COMMANDS_MENU = f"""
Assistant bot's commands menu:
 - contact -
 add <name> <number> \t\t# add new single contact to phone book
 change <name> <new_number> \t# change contact's number
 phone <name> \t\t\t# show contact's phone number by its name (if exist)
 delete <name> \t\t\t# delete all contact info
 all\t\t\t\t# show all contacts in the book
 - birthdays -
 birthday-add <name> <date> \t# add contact's birthday
 birthday-show <name>\t\t# show contact's birthday
 birthday-in <days>\t\t# show birthdays next week
 - notes -
 note-add <text_note>\t\t# add note
 note-show-all\t\t\t# add note
 note-edit <id>\t\t\t# edit note by id
 note-delete <id>\t\t# delete note by id
 - leave - 
 exit | close \t\t\t# exit from assistant
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


class PhoneNumberDoesNotExist(Exception):
    pass


class AlreadyExistsError(Exception):
    pass


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, name):
        super().__init__(name)


class Phone(Field):
    def __init__(self, phone):
        pattern = re.compile(r"\d{10}")
        if re.search(pattern, phone):
            super().__init__(phone)
        else:
            raise PhoneNumberDoesNotExist


class Birthday(Field):
    def __init__(self, bday: str):
        try:
            bd = dt.strptime(bday, "%d.%m.%Y")
            super().__init__(bd)
        except ValueError:
            raise ValueError


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        try:
            self.phones.append(Phone(phone))
        except PhoneNumberDoesNotExist:
            pass

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p.value

    def remove_phone(self, phone):
        i = 0
        for p in self.phones:
            if p.value == phone:
                self.phones.pop(i)
            i += 1

    def edit_phone(self, old, new):
        for p in self.phones:
            p.value = new if p.value == old else p.value

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):

    def add_record(self, record: Record):
        self.data[str(record.name)] = record

    def find(self, name):
        return self.data[name]

    def all(self):
        print(
            f"{const.COLOR_BOOK}Full address book [numbers in base: {len(self.data)}]:"
        )
        table = PrettyTable()
        table.field_names = ["Name", "Phone(s)", "e-mail", "birthday"]
        # print(self.items())
        for k in self.data.keys():
            print(self.data[k])
            # table.add_row(k, "na", "na", "na"])

        print(table)

    def delete(self, name):
        self.data.pop(name, None)

    def get_upcoming_birthdays(self, days):

        notifications = []

        # get today values: date, year, number of the current day in year and total days is year

        # use next two lines to check fuctionality
        # today_date = dt.(2024, 12, 30).date()
        today_date = dt.today().date()

        today_year = today_date.year
        today_number_in_year = today_date.timetuple().tm_yday
        ny_number_in_year = dt(today_year, 12, 31).timetuple().tm_yday

        for name, record in self.data.items():

            # for current user found
            # his original birth date
            # his birthday this year
            # day number of birthday in year
            user_bd_original = record.birthday.value
            user_bd_this_year = dt(
                year=today_year, month=user_bd_original.month, day=user_bd_original.day
            ).date()
            user_bd_this_year_number = user_bd_this_year.timetuple().tm_yday

            # simple situation if birthday within a week from now
            if 0 <= user_bd_this_year_number - today_number_in_year <= 7:

                congratulation_date = user_bd_this_year

                # weekend days check and move date to monday if true
                if congratulation_date.isoweekday() >= 6:
                    congratulation_date += tdelta(8 - congratulation_date.isoweekday())

                # create and append dict to result list
                user_to_congratulate = {}
                user_to_congratulate["name"] = name
                user_to_congratulate["congratulation_date"] = (
                    congratulation_date.strftime("%d.%m.%Y")
                )
                notifications.append(user_to_congratulate)

            # situation at the end of year and birthday on january begin
            elif (
                ny_number_in_year - today_number_in_year + user_bd_this_year_number <= 7
            ):

                # congratulation_date must be set to next year
                congratulation_date = dt(
                    year=today_year + 1,
                    month=user_bd_original.month,
                    day=user_bd_original.day,
                )

                # weekend days check and move date to monday if true
                if congratulation_date.isoweekday() >= 6:
                    congratulation_date += tdelta(8 - congratulation_date.isoweekday())

                # create and append dict to result list
                user_to_congratulate = {}
                user_to_congratulate["name"] = name
                user_to_congratulate["congratulation_date"] = (
                    congratulation_date.strftime("%d.%m.%Y")
                )
                notifications.append(user_to_congratulate)

        return notifications


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = Record(name)
    record.add_phone(phone)
    book.add_record(record)


@input_error
def change_contact(args, book: AddressBook):
    name, old_phone, new_phone, *_ = args
    record = book.find(name)
    record.edit_phone(old_phone, new_phone)


@input_error
def phone(args, book: AddressBook):
    name, *_ = args
    record = book.find(name)
    print(record)


@input_error
def delete(args, book: AddressBook):
    name, *_ = args
    record = book.delete(name)


@input_error
def all(book: AddressBook):
    book.all()


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

        elif command == "add":
            print(f"{const.COLOR_MENU}{COMMANDS_MENU}")
            add_contact(args, book)

        elif command == "change":
            print(f"{const.COLOR_MENU}{COMMANDS_MENU}")
            change_contact(args, book)

        elif command == "phone":
            print(f"{const.COLOR_MENU}{COMMANDS_MENU}")
            phone(args, book)

        elif command == "delete":
            print(f"{const.COLOR_MENU}{COMMANDS_MENU}")
            delete(args, book)

        elif command == "all":
            print(f"{const.COLOR_MENU}{COMMANDS_MENU}")
            all(book)

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
