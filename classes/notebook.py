from modules import const                               # Import constants used for formatting and colors

from collections import UserDict                        # UserDict for creating a dictionary-like class
from classes.note import Note                           # Import the Note class for managing individual notes
from prettytable import PrettyTable                     # Import PrettyTable for formatted table output

# Basic NOTEBOOK class for managing a collection of notes
class NoteBook(UserDict):
    def __init__(self):
        super().__init__()                              # Initialize the parent UserDict class
        self.note_counter = 1                           # Initialize a counter for note IDs

    def add_note(self):
        """Add a new note to the notebook."""
        note_id = str(self.note_counter)                # Create a note ID based on the counter
        note_text = input("Enter the text: ")           # Prompt user for note text
        tags = input("Enter the tag (starts with #): ") # Prompt user for tags
        note = Note(note_text, note_id, tags)           # Create a new Note instance
        self.data[note_id] = note                       # Store the note in the dictionary
        self.note_counter += 1                          # Increment the note counter for the next note
        return note_id                                  # Return the ID of the newly added note

    def delete_note(self, note_id):
        """Delete a note from the notebook by its ID."""
        try:
            del self.data[note_id]                      # Remove the note from the dictionary
        except KeyError:
            raise KeyError                              # Raise an error if the note ID does not exist

    def edit_note(self, note_id, new_text):
        """Edit the text of a note by its ID."""
        try:
            self.data[note_id].edit(new_text)           # Update the note text
        except KeyError:
            raise KeyError                              # Raise an error if the note ID does not exist

    def show_all_notes(self):
        """Display all notes in the notebook."""
        if not self.data:                               # Check if there are no notes
            print(f"{const.COLOR_ERROR}No notes found") # Print error message

        print(f"{const.COLOR_BOOK}Full note book [numbers in base: {len(self.data)}]")  # Print note count
        table = PrettyTable()                                                           # Create a table for formatted output
        table.field_names = ["ID", "Note Text", "Tag"]                                  # Define table headers

        for note_id, note in self.data.items():                                         # Iterate through all notes
            table.add_row(
                [
                    note.note_id,                                                       # Note ID
                    note.note_text,                                                     # Note text
                    ", ".join(note.tags) if note.tags else "No tag",                    # Tags or "No tag" if none
                ],
                divider=True,                                                           # Add a divider between rows
            )

        print(table)                                                                    # Print the formatted table of notes