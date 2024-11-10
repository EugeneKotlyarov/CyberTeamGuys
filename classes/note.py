from typing import Optional, List, Dict             # Import type hints for better type checking

# Class NOTE represents a single record in a notebook
class Note:
    id: int                                         # Unique identifier for the note
    text: str                                       # Text content of the note
    tags: List[str] = None                          # List of tags associated with the note

    def __init__(self, note_text, note_id, tags=None):
        self.note_text = note_text                  # Initialize note text
        self.note_id = note_id                      # Initialize note ID
        self.tags = self._extract_tags(tags)        # Initialize tags by extracting from input

    def _extract_tags(self, tags: str) -> List[str]:
        """Extract tags from the given string."""
        if tags:
            # Return a list of tags, removing the '#' prefix
            return [tag[1:] for tag in tags.split() if tag.startswith("#")]
        return ["No tag"]                           # Default no tag if none are provided

    def add_tag(self, tags):
        """Add a new tag to the note if it doesn't already exist."""
        if tags not in self.tags:
            self.tags.append(tags)                  # Append the new tag to the list

    def edit(self, new_text):
        """Edit the text of the note."""
        self.note_text = new_text                   # Update the note text

    def __str__(self):
        """Return a string representation of the note."""
        tags = " ".join(self.tags) if self.tags else "No tags"                      # Format tags for display
        return f"Note ID: {self.note_id} | Text: {self.note_text} | Tag: {tags}"    # Return formatted string