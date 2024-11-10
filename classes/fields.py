from classes.exceptions import InvalidFormat    # Import custom exception for invalid formats

import re                                       # Regular expression module for pattern matching
from datetime import datetime as dt             # Import datetime for date manipulations


# Basic structure for a contact card in an address book:
# Each contact has NAME, PHONE, BIRTHDAY, and EMAIL fields
# Includes validation checks for phone and email formats

class Field:
    """Base class for all fields in a contact card."""
    def __init__(self, value):
        self.value = value                      # Initialize the field with a value

    def __str__(self):
        return str(self.value)                  # Return the string representation of the field value


class Name(Field):
    """Class representing a contact's name."""
    def __init__(self, name):
        super().__init__(name)                  # Initialize with the name value


class Phone(Field):
    """Class representing a contact's phone number with validation."""
    def __init__(self, phone):
        # Regular expression pattern for valid phone numbers (10 to 15 digits, optional +)
        pattern = re.compile(r"^\+?\d{10,15}$")
        if re.search(pattern, phone):           # Validate the phone number format
            super().__init__(phone)             # Initialize with the valid phone number
        else:
            raise InvalidFormat                 # Raise an exception if the format is invalid


class Birthday(Field):
    """Class representing a contact's birthday with validation."""
    def __init__(self, bday: str):
        try:
            # Parse the birthday string into a date object
            bd = dt.strptime(bday, "%Y-%m-%d").date()
            super().__init__(bd)                # Initialize with the valid date object
        except ValueError:
            raise InvalidFormat                 # Raise an exception if the format is invalid


class Email(Field):
    """Class representing a contact's email address with validation."""
    def __init__(self, email: str):
        # Regular expression pattern for valid email addresses
        pattern = re.compile(r"^[\w\.-]+@[\w\.-]+\.\w+$")
        if re.search(pattern, email):           # Validate the email format
            super().__init__(email)             # Initialize with the valid email address
        else:
            raise InvalidFormat                 # Raise an exception if the format is invalid