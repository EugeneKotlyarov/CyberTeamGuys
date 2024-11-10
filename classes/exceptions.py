# Define a custom exception to handle invalid formats in user input
class InvalidFormat(Exception):
    """Exception raised for errors in the input format."""
    pass  # Inherits from the base Exception class without additional functionality