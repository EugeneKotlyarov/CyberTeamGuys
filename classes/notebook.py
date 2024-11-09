
from collections import UserDict
from classes.note import Note
from prettytable import PrettyTable


class NoteBook(UserDict):
    def __init__(self):
        super().__init__()
        self.note_counter = 1

    def add_note(self, note_text, tags = None):
        note_id = str(self.note_counter)
        note_text = input("Enter the text: ")
        tags = input("Enter the tag: ")
        note = Note(note_text, note_id, str(tags))
        self.data[note_id] = note
        self.note_counter += 1
        return f"Note added with ID: {note_id}"

    def delete_note(self, note_id):
        if note_id in self.data:
            del self.data[note_id]
            return f"Note with ID {note_id} deleted."
        return "Note not found."

    def edit_note(self, note_id, new_text):
        if note_id in self.data:
            self.data[note_id].edit(new_text)
            return f"Note with ID {note_id} updated."
        return "Note not found."

    def show_all_notes(self):
        if not self.data:
            return "No notes found."
        
        table = PrettyTable()
        table.field_names = ["ID", "Note Text", "Tag"]
    
        for note_id, note in self.data.items():
            table.add_row([note.note_id, note.note_text, ", " .join(note.tags) if note.tags else "No tag"])

        return table.get_string()
