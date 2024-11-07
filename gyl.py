''''
a console bot helper that recognizes commands entered from the keyboard 
and responds accordingly.
The phone number must be in 10-digit format

Comand list:
"hello"
"add [Name] [Phone number]"
"change [Name] [Phone number]"
"phone [Name]"
"remove [Name] [Phone number]"
"delete [Name]"
"all" - command that shows all numbers and phones in the notebook
"close" or "exit"
"birthdays" - the comand that shows the birthday for the next week
"add-birthday [Name] [Date (DD.MM.YYYY)]"
"show-birthday" [Name]
'''
#
#we implement class
#
from collections import UserDict
from datetime import datetime, timedelta
import pickle

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        if self.validate(value):
            super().__init__(value)
        else:
            raise ValueError("Phone number must contain exactly 10 digits.")

    @staticmethod
    def validate(phone_number):
        return phone_number.isdigit() and len(phone_number) == 10
    
class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone_number):
        if phone_number not in [phone.value for phone in self.phones]:
            phone = Phone(phone_number)
            self.phones.append(phone)
            return "Phone number added."
        return "This phone number already exists."

    def edit_phone(self, old_number, new_number):
        for phone in self.phones:
            if phone.value == old_number:
                phone.value = new_number
                return "Phone number updated."
        return "Old phone number not found."

    def remove_phone(self, phone_number):
        for phone in self.phones:
            if phone.value == phone_number:
                self.phones.remove(phone)
                return "Phone number removed."
        return "Phone number not found."

    def find_phone(self, phone_number):
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
        return None
    
    def add_birthday(self, birthday_date):
        if not self.birthday:
            self.birthday = Birthday(birthday_date)
            return "Birthday added."
        return "Birthday already exists."
    
    def days_to_birthday(self):
        if self.birthday:
            today = datetime.now().date()
            next_birthday = self.birthday.value.replace(year=today.year)
            if next_birthday < today:
                next_birthday = next_birthday.replace(year=today.year + 1)
            return (next_birthday - today).days
        return None
    
    def show_birthday(self):
        if self.birthday:
            return f"{self.name.value}'s birthday is on {self.birthday.value.strftime('%d.%m.%Y')}"
        return "Birthday not set."

    def __str__(self):
        phones = "; ".join(phone.value for phone in self.phones)
        return f"Contact name: {self.name.value}, phones: {phones if phones else 'No phones'}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name, None)

    def delete(self, name):
        if name in self.data:
            del self.data[name]
            return "Contact deleted."
        return "Contact not found."

    def show_all(self):
        if not self.data:
            return "No contacts saved."
        return "\n".join(str(record) for record in self.data.values())
    
    def get_upcoming_birthdays(self, days=7):
        today = datetime.now().date()
        upcoming_birthdays = []
        for record in self.data.values():
            if record.birthday:
                next_birthday = record.birthday.value.replace(year=today.year)
                if today <= next_birthday <= today + timedelta(days=days):
                    upcoming_birthdays.append(f"{record.name.value} - {next_birthday.strftime('%d.%m.%Y')}")
        return "\n".join(upcoming_birthdays) if upcoming_birthdays else "No upcoming birthdays."
    def save(self, filename="addressbook.pkl"):
        with open(filename, "wb") as f:
            pickle.dump(self, f)

    @classmethod
    def load(cls, filename="addressbook.pkl"):
        try:
            with open(filename, "rb") as f:
                return pickle.load(f)
        except FileNotFoundError:
            return cls()

class Bot:
    def __init__(self):
        self.address_book = AddressBook.load()

    def input_error(func):
        def inner(self, *args):
            try:
                return func(self, *args)
            except ValueError:
                return "Give me a valid name and phone number (10 digits)."
            except KeyError:
                return "Contact not found."
            except IndexError:
                return "Please provide the necessary arguments."
        return inner

    @input_error
    def add_contact(self, name, phone):
        record = self.address_book.find(name)
        if record:
            return record.add_phone(phone)
        else:
            new_record = Record(name)
            new_record.add_phone(phone)
            self.address_book.add_record(new_record)
            return "Contact added."
        
    @input_error
    def add_birthday(self, name, birthday):
        record = self.address_book.find(name)
        if record:
            return record.add_birthday(birthday)
        else:
            raise KeyError
        
    def birthdays(self):
        return self.address_book.get_upcoming_birthdays()
    
    @input_error
    def show_birthday(self, name):
        record = self.address_book.find(name)
        if record:
            return record.show_birthday()
        else:
            return "Contact not found."

    @input_error
    def change_contact(self, name, new_phone):
        record = self.address_book.find(name)
        if record:
            return record.edit_phone(record.phones[0].value, new_phone)  # Edit the first phone number
        raise KeyError

    @input_error
    def get_phone(self, name):
        record = self.address_book.find(name)
        if record:
            return f"{name}'s phone number(s): " + ", ".join(phone.value for phone in record.phones)
        else:
            raise KeyError

    @input_error
    def remove_phone(self, name, phone):
        record = self.address_book.find(name)
        if record:
            return record.remove_phone(phone)
        else:
            raise KeyError

    @input_error
    def delete_contact(self, name):
        return self.address_book.delete(name)

    def handle_command(self, command, args):
        if command == "hello":
            return "How can I help you?"
        elif command == "add" and len(args) == 2:
            return self.add_contact(args[0], args[1])
        elif command == "add-birthday" and len(args) == 2:
            return self.add_birthday(args[0], args[1])
        elif command == "change" and len(args) == 2:
            return self.change_contact(args[0], args[1])
        elif command == "phone" and len(args) == 1:
            return self.get_phone(args[0])
        elif command == "remove" and len(args) == 2:
            return self.remove_phone(args[0], args[1])
        elif command == "delete" and len(args) == 1:
            return self.delete_contact(args[0])
        elif command == "show-birthday" and len(args) == 1:
            return self.show_birthday(args[0])
        elif command == "birthdays":
            return self.address_book.get_upcoming_birthdays()
        elif command == "all":
            return self.address_book.show_all()
        elif command in ["close", "exit"]:
            return "Good bye!"
        else:
            return "Invalid command."

    def start(self):
        print("Welcome to the assistant bot!")
        while True:
            user_input = input("Enter a command: ")
            command, *args = user_input.split(maxsplit=2)
            answer = self.handle_command(command, args)
            print(answer)
            if answer == "Good bye!":
                self.address_book.save()
                break

if __name__ == "__main__":
    bot = Bot()
    bot.start()