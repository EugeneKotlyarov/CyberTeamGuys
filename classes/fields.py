from exceptions import PhoneNumberDoesNotExist

import re
from datetime import datetime as dt
from datetime import timedelta as tdelta


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
            bd = dt.strptime(bday, "%Y-%m-%d").date()
            super().__init__(bd)
        except ValueError:
            raise ValueError


class Email(Field):
    def __init__(self, email: str):
        super().__init__(email)
