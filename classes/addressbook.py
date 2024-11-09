from classes.record import Record

from modules.errors import input_error
from modules import const

from collections import UserDict
from colorama import Style
from datetime import datetime as dt
from datetime import timedelta as tdelta
from prettytable import PrettyTable


# basic ADDRESSBOOK class with
# function ADD_RECORD for adding contact card in a BOOK
# function FIND to search contact card by its name in a BOOK
# function ALL simply prints BOOK
# function DELETE deletes contact from book
# function GET_UPCOMING_BIRTHDAYS prints table for congratulations


class AddressBook(UserDict):

    def add_record(self, record: Record):
        self.data[str(record.name)] = record

    def find(self, name):
        return self.data[name]

    def all(self):
        print(
            f"{const.COLOR_BOOK}Full address book [numbers in base: {len(self.data)}]"
        )
        table = PrettyTable()
        table.field_names = ["Name", "Phone(s)", "birthday", "e-mail"]
        print_data = {}
        for i in self.data.values():
            print_data.update()
            table.add_row(
                [i.name, "\n".join(j.value for j in i.phones), i.birthday, i.email],
                divider=True,
            )
        print(table)

    def delete(self, name):
        self.data.pop(name, None)

    def get_upcoming_birthdays(self, days: int):

        if days < 0 or days > 31:
            print(
                f"{const.COLOR_ERROR}Enter rational days number, between 1 and 31, otherwise it doesn't make sence"
            )
            return None

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
            if record.birthday:
                user_bd_original = record.birthday.value
                user_bd_this_year = dt(
                    year=today_year,
                    month=user_bd_original.month,
                    day=user_bd_original.day,
                ).date()
                user_bd_this_year_number = user_bd_this_year.timetuple().tm_yday

                # simple situation if birthday within a week from now
                if 0 <= user_bd_this_year_number - today_number_in_year <= days:

                    congratulation_date = user_bd_this_year

                    # weekend days check and move date to monday if true
                    if congratulation_date.isoweekday() >= 6:
                        congratulation_date += tdelta(
                            8 - congratulation_date.isoweekday()
                        )

                    # create and append dict to result list
                    user_to_congratulate = {}
                    user_to_congratulate["name"] = name
                    user_to_congratulate["congratulation_date"] = (
                        congratulation_date.strftime("%d.%m.%Y")
                    )
                    notifications.append(user_to_congratulate)

                # situation at the end of year and birthday on january begin
                elif (
                    ny_number_in_year - today_number_in_year + user_bd_this_year_number
                    <= days
                ):

                    # congratulation_date must be set to next year
                    congratulation_date = dt(
                        year=today_year + 1,
                        month=user_bd_original.month,
                        day=user_bd_original.day,
                    )

                    # weekend days check and move date to monday if true
                    if congratulation_date.isoweekday() >= 6:
                        congratulation_date += tdelta(
                            8 - congratulation_date.isoweekday()
                        )

                    # create and append dict to result list
                    user_to_congratulate = {}
                    user_to_congratulate["name"] = name
                    user_to_congratulate["congratulation_date"] = (
                        congratulation_date.strftime("%d.%m.%Y")
                    )
                    notifications.append(user_to_congratulate)

        if notifications:
            print(
                f"{const.COLOR_BOOK}In next {days} days, such people has their birthdays:"
            )
            table = PrettyTable()
            table.field_names = ["Name", "Congratulation Date"]
            print_data = {}
            for i in notifications:
                print_data.update()
                table.add_row(
                    [i["name"], i["congratulation_date"]],
                    divider=True,
                )
            print(table)
