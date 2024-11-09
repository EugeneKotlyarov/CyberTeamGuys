from classes.exceptions import InvalidFormat

import re
from datetime import datetime as dt


# basic sctructure for contact card in a BOOK:
# NAME, PHONE, BIRTHDAY, EMAIL all type FIELD
# added phone and email validation check


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
        pattern = re.compile(r"^\+?\d{10,15}$")
        if re.search(pattern, phone):
            super().__init__(phone)
        else:
            raise InvalidFormat


class Birthday(Field):
    def __init__(self, bday: str):
        try:
            bd = dt.strptime(bday, "%Y-%m-%d").date()
            super().__init__(bd)
        except ValueError:
            raise InvalidFormat


class Email(Field):
    def __init__(self, email: str):
        pattern = re.compile(r"^[\w\.-]+@[\w\.-]+\.\w+$")
        if re.search(pattern, email):
            super().__init__(email)
        else:
            raise InvalidFormat
