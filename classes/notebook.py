from modules import const

from collections import UserDict
from classes.note import Note
from prettytable import PrettyTable


class NoteBook(UserDict):
    def __init__(self):
        super().__init__()
        self.note_counter = 1

    def add_note(self):
        note_id = str(self.note_counter)
        note_text = input("Enter the text: ")
        tags = input("Enter the tag (starts with #): ")
        note = Note(note_text, note_id, tags)
        self.data[note_id] = note
        self.note_counter += 1
        return note_id

    def delete_note(self, note_id):
        # if note_id in self.data:
        try:
            del self.data[note_id]
            # return f"Note with ID {note_id} deleted"
        except KeyError:
            raise KeyError
        # return "Note not found"

    def edit_note(self, note_id, new_text):
        # if note_id in self.data:
        try:
            self.data[note_id].edit(new_text)
        except KeyError:
            raise KeyError
            # return f"Note with ID {note_id} updated."
        # return "Note not found."

    def show_all_notes(self):
        if not self.data:
            print(f"{const.COLOR_ERROR}No notes found")

        print(f"{const.COLOR_BOOK}Full note book [numbers in base: {len(self.data)}]")
        table = PrettyTable()
        table.field_names = ["ID", "Note Text", "Tag"]

        for note_id, note in self.data.items():
            table.add_row(
                [
                    note.note_id,
                    note.note_text,
                    ", ".join(note.tags) if note.tags else "No tag",
                    # note.tags
                ],
                divider=True,
            )

        print(table)
