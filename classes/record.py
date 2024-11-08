from classes.exceptions import PhoneNumberDoesNotExist

from classes.fields import Name, Phone, Birthday, Email


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.email = None
        self.birthday = None

    def phone_add(self, phone):
        self.phones.append(Phone(phone))

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

    def birthday_add(self, birthday):
        self.birthday = Birthday(birthday)

    def email_add(self, email):
        self.email = Email(email)

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"
