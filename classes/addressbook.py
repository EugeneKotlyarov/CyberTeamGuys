from classes.record import Record           # Import the Record class for contact details

from modules.errors import input_error      # Custom error handling for user input
from modules import const                   # Import constants used in the program

from collections import UserDict            # UserDict allows us to create a dictionary-like class
from colorama import Style                  # For colored terminal output
from datetime import datetime as dt         # For date and time manipulations
from datetime import timedelta as tdelta    # For representing time durations
from prettytable import PrettyTable         # For creating formatted tables in the console


# Basic ADDRESSBOOK class with methods for managing contacts
class AddressBook(UserDict):

    # Method to add a record (contact) to the address book
    def add_record(self, record: Record):
        self.data[str(record.name)] = record

    # Method to find a record by name
    def find(self, name):
        return self.data[name]

    # Method to display all contacts in the address book
    def all(self):
        print(
            f"{const.COLOR_BOOK}Full address book [numbers in base: {len(self.data)}]"
        )                                                                               # Print the total number of contacts
        table = PrettyTable()                                                           # Create a table for formatted output
        table.field_names = ["Name", "Phone(s)", "Birthday", "E-mail"]                  # Define table headers
        print_data = {}                                                                 # Initialize a dictionary for storing data (unused)
        for i in self.data.values():                                                    # Iterate through all records
            print_data.update()                                                         # Update print_data (currently does nothing)
            table.add_row(
                [i.name, "\n".join(j.value for j in i.phones), i.birthday, i.email],
                divider=True,
            )                                                                           # Add a row for each contact
        print(table)                                                                    # Print the table

    # Method to delete a record by name
    def delete(self, name):
        self.data.pop(name, None)

    # Method to print upcoming birthdays within a specified number of days
    def get_upcoming_birthdays(self, days: int):
        # Validate the number of days
        if days < 0 or days > 31:
            print(
                f"{const.COLOR_ERROR}Enter a rational number of days, between 1 and 31, otherwise it doesn't make sense"
            )
            return None  # Return if the input is invalid

        notifications = []

        # Get today's date and relevant values
        today_date = dt.today().date()
        today_year = today_date.year
        today_number_in_year = today_date.timetuple().tm_yday
        ny_number_in_year = dt(today_year, 12, 31).timetuple().tm_yday

        for name, record in self.data.items():                                      # Iterate through all contacts
            if record.birthday:                                                     # Check if the contact has a birthday set
                user_bd_original = record.birthday.value                            # Original birthday date
                user_bd_this_year = dt(
                    year=today_year,
                    month=user_bd_original.month,
                    day=user_bd_original.day,
                ).date()                                                            # Birthday date for the current year
                user_bd_this_year_number = user_bd_this_year.timetuple().tm_yday    # Day of the year for birthday

                # Check if the birthday is within the specified range
                if 0 <= user_bd_this_year_number - today_number_in_year <= days:
                    congratulation_date = user_bd_this_year                         # Set congratulation date

                    # Check for weekend and adjust to the following Monday if true
                    if congratulation_date.isoweekday() >= 6:
                        congratulation_date += tdelta(
                            8 - congratulation_date.isoweekday()
                        )

                    # Create a notification dictionary for the user
                    user_to_congratulate = {}
                    user_to_congratulate["name"] = name
                    user_to_congratulate["congratulation_date"] = (
                        congratulation_date.strftime("%d.%m.%Y")
                    )  # Format the date for output
                    notifications.append(user_to_congratulate)

                # Handle birthdays that fall at the end of the year
                elif (
                    ny_number_in_year - today_number_in_year + user_bd_this_year_number
                    <= days
                ):
                    # Set congratulation date to next year
                    congratulation_date = dt(
                        year=today_year + 1,
                        month=user_bd_original.month,
                        day=user_bd_original.day,
                    )

                    # Check for weekend and adjust to the following Monday if true
                    if congratulation_date.isoweekday() >= 6:
                        congratulation_date += tdelta(
                            8 - congratulation_date.isoweekday()
                        )

                    # Create a notification dictionary for the user
                    user_to_congratulate = {}
                    user_to_congratulate["name"] = name 
                    user_to_congratulate["congratulation_date"] = (
                        congratulation_date.strftime("%d.%m.%Y")
                    )  # Format the date for output
                    notifications.append(user_to_congratulate)

        # Print notifications if there are any upcoming birthdays
        if notifications:
            print(
                f"{const.COLOR_BOOK}In next {days} days, such people have their birthdays:"
            )
            table = PrettyTable()                                   # Create a table for displaying notifications
            table.field_names = ["Name", "Congratulation Date"]     # Define table headers
            print_data = {}                                         # Initialize a dictionary for storing data (unused)
            for i in notifications:                                 # Iterate through notifications
                print_data.update()                                 # Update print_data (currently does nothing)
                table.add_row(
                    [i["name"], i["congratulation_date"]],
                    divider=True,
                )                                                   # Add a row for each notification
            print(table)                                            # Print the table of upcoming birthdays