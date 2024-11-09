from modules import const
from classes.exceptions import InvalidFormat


class AlreadyExistsError(Exception):
    pass


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            match func.__name__:
                case "add_contact":
                    print(f"{const.COLOR_ERROR}Give me name and phone please")
                case "card_edit":
                    print(
                        f"{const.COLOR_ERROR}Give me name, old and new phone for contact please"
                    )
                case "card":
                    print(f"{const.COLOR_ERROR}Give me name to search")
                case "birthday_show":
                    print(
                        f"{const.COLOR_ERROR}Give me name to search for a birthday data"
                    )
                case "birthday_in":
                    print(f"{const.COLOR_ERROR}Please, specify days number as integer")

        except KeyError:
            match func.__name__:
                case "card_edit":
                    print(
                        f"{const.COLOR_ERROR}Contact was not found. Nothing to change"
                    )
                case "birthday_add":
                    print(f"{const.COLOR_ERROR}Contact was not found")
                case "birthday_show":
                    print(f"{const.COLOR_ERROR}Contact was not found")
                case "note_delete":
                    print(f"{const.COLOR_ERROR}Note was not found")
                case "note_edit":
                    print(f"{const.COLOR_ERROR}Note was not found")

        except AttributeError:
            match func.__name__:
                case "birthday_in":
                    print(f"{const.COLOR_ERROR}No one record has a birthday value")

        except AlreadyExistsError:
            print(
                f'{const.COLOR_ERROR}Contact WAS NOT added. Already exists. Please use "change" command for edit'
            )

        except InvalidFormat:
            match func.__name__:
                case "card_add_phone":
                    print(
                        f"{const.COLOR_ERROR}Please enter number in 10to15 digits format, (can start with +)"
                    )
                case "birthday_add":
                    print(
                        f"{const.COLOR_ERROR}Invalid date format for Birthday value, please use format: YYYY-MM-DD"
                    )
                case "email_add":
                    print(f"{const.COLOR_ERROR}Please enter a valid e-mail")

    return inner


def main():
    pass


if __name__ == "__main__":
    main()
