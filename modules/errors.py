from modules import const

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
                case "change_contact":
                    print(
                        f"{const.COLOR_ERROR}Give me name, old and new phone for contact please"
                    )
                case "phone":
                    print(f"{const.COLOR_ERROR}Give me name to search")
                case "add_birthday":
                    print(
                        f"{const.COLOR_ERROR}Invalid date format for Birthday value, please use format: DD.MM.YYYY"
                    )
                case "show_birthday":
                    print(f"{const.COLOR_ERROR}Give me name to search for a birthday data")

        except KeyError:
            match func.__name__:
                case "change_contact":
                    print(
                        f'{const.COLOR_ERROR}Contact WAS NOT found. Nothing to change. Use "add" command to create one'
                    )
                case "phone":
                    print(
                        f'{const.COLOR_ERROR}Contact WAS NOT found. Please use "add" command to create one'
                    )

        except AttributeError:
            match func.__name__:
                case "birthdays":
                    print(f"{const.COLOR_ERROR}No one record has a birthday value")

        except AlreadyExistsError:
            print(
                f'{const.COLOR_ERROR}Contact WAS NOT added. Already exists. Please use "change" command for edit'
            )

    return inner


def main():
    pass


if __name__ == "__main__":
    main()
