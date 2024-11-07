import pickle
import re
from collections import UserDict
from colorama import Fore, Back, Style
from datetime import datetime as dt
from datetime import timedelta as tdelta


def main():

    # Створення нової адресної книги або через відновлення
    book = load_data()

    while True:
        print(f"{COLOR_MENU}{COMMANDS_MENU}")
        user_input = input(f"Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print(f"{COLOR_DONE}\nGood bye!")
            save_data(book)
            break

        elif command == "add":
            add_contact(args, book)

        elif command == "change":
            change_contact(args, book)

        elif command == "phone":
            phone(args, book)

        elif command == "all":
            all(book)

        elif command == "add-birthday":
            add_birthday(args, book)

        elif command == "show-birthday":
            show_birthday(args, book)

        elif command == "birthdays":
            birthdays(book)

        elif command == "hello":
            print(f"{COLOR_DONE}\nHow can I help you?")

        else:
            print(f"\n{COLOR_ERROR}Invalid command")


if __name__ == "__main__":
    main()
