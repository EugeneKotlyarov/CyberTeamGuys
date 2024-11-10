from modules import const                       # Import constants for colored output
from classes.exceptions import InvalidFormat    # Import custom exception for invalid formats

# This is a DECORATOR
# It handles exceptions for functions in the main application
# All ERROR cases in this module are managed here

def input_error(func):
    """Decorator to handle input errors for decorated functions."""
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)        # Call the original function
        except ValueError:
            # Handle ValueError exceptions for specific functions
            match func.__name__:
                case "add_contact":
                    print(f"{const.COLOR_ERROR}Give me name and phone please")
                case "card_edit":
                    print(f"{const.COLOR_ERROR}Give me name, old and new phone for contact please")
                case "card":
                    print(f"{const.COLOR_ERROR}Give me name to search")
                case "birthday_show":
                    print(f"{const.COLOR_ERROR}Give me name to search for a birthday data")
                case "birthday_in":
                    print(f"{const.COLOR_ERROR}Please, specify days number as integer")

        except KeyError:
            # Handle KeyError exceptions for specific functions
            match func.__name__:
                case "card_edit":
                    print(f"{const.COLOR_ERROR}Contact was not found. Nothing to change")
                case "birthday_add":
                    print(f"{const.COLOR_ERROR}Contact was not found")
                case "birthday_show":
                    print(f"{const.COLOR_ERROR}Contact was not found")
                case "note_delete":
                    print(f"{const.COLOR_ERROR}Note was not found")
                case "note_edit":
                    print(f"{const.COLOR_ERROR}Note was not found")

        except AttributeError:
            # Handle AttributeError for specific functions
            match func.__name__:
                case "birthday_in":
                    print(f"{const.COLOR_ERROR}No one record has a birthday value")

        except InvalidFormat:
            # Handle InvalidFormat exceptions for specific functions
            match func.__name__:
                case "card_add_phone":
                    print(f"{const.COLOR_ERROR}Please enter number in 10 to 15 digits format, (can start with +)")
                case "birthday_add":
                    print(f"{const.COLOR_ERROR}Invalid date format for Birthday value, please use format: YYYY-MM-DD")
                case "email_add":
                    print(f"{const.COLOR_ERROR}Please enter a valid e-mail")

    return inner                                # Return the inner function wrapped by the decorator

def main():
    pass                                        # Placeholder for the main function

if __name__ == "__main__":
    main()                                      # Execute the main function if the script is run directly