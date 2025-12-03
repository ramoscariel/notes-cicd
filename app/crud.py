from typing import List
from app.models import Note, NoteCreate


# Simulación DB en Memoria
db: List[Note] = []
next_id = 1


def create_note(note: NoteCreate) -> Note:
    global next_id
    new_note = Note(id=next_id, **note.model_dump())
    db.append(new_note)
    next_id += 1
    return new_note


def get_notes() -> List[Note]:
    return db


def get_note_by_id(note_id: int) -> Note | None:
    for n in db:
        if n.id == note_id:
            return n
    return None


def delete_note(note_id: int) -> bool:
    note = get_note_by_id(note_id)

    if note is None:
        return False

    db.remove(note)
    return True
