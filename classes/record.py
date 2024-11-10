from classes.fields import Name, Phone, Birthday, Email # Import field classes for contact details

# Class RECORD represents a single record in the address book
# with basic functions to ADD, FIND, EDIT, etc. for managing contact cards
class Record:
    def __init__(self, name):
        self.name = Name(name)                          # Initialize the contact's name
        self.phones = []                                # List to store multiple phone numbers
        self.email = None                               # Initialize email as None
        self.birthday = None                            # Initialize birthday as None

    def phone_add(self, phone):
        """Add a new phone number to the contact."""
        self.phones.append(Phone(phone))                # Create a Phone instance and append it to the list

    def find_phone(self, phone):
        """Find and return a phone number if it exists."""
        for p in self.phones:                           # Iterate through the list of phone numbers
            if p.value == phone:                        # Check if the phone number matches
                return p.value                          # Return the found phone number

    def remove_phone(self, phone):
        """Remove a phone number from the contact."""
        i = 0                                           # Initialize index for tracking position in the list
        for p in self.phones:                           # Iterate through the list of phone numbers
            if p.value == phone:                        # Check if the phone number matches
                self.phones.pop(i)                      # Remove the phone number from the list
                return                                  # Exit after removing the first match
            i += 1                                      # Increment index

    def edit_phone(self, old, new):
        """Edit an existing phone number."""
        for p in self.phones:                               # Iterate through the list of phone numbers
            p.value = new if p.value == old else p.value    # Update the phone number if it matches the old one

    def birthday_add(self, birthday):
        """Add a birthday to the contact."""
        self.birthday = Birthday(birthday)                  # Create a Birthday instance

    def email_add(self, email):
        """Add an email address to the contact."""
        self.email = Email(email)                           # Create an Email instance

    def __str__(self):
        """Return a string representation of the contact record."""
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"  # Format the output