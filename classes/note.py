from typing import Optional, List, Dict

class Note:
    id: int
    text: str
    tags: List[str] = None

    def __init__(self, note_text, note_id, tags=None):
        self.note_text = note_text
        self.note_id = note_id
        self.tags = self._extract_tags(tags)

    def _extract_tags(self, tags: str) -> List[str]:
        if tags:
            return [tag[1:] for tag in tags.split() if tag.startswith('#')]
        return "No tag"


    def add_tag(self, tags):
        if tags not in self.tags:
            self.tags.append(tags)

    def edit(self, new_text):
        self.note_text = new_text

    def __str__(self):
        tags = " ".join(self.tags) if self.tags else "No tags"
        return f"Note ID: {self.note_id} | Text: {self.note_text} | Tag: {tags}"