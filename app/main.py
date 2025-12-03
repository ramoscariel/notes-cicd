from fastapi import FastAPI, HTTPException
from app.crud import create_note, get_note_by_id, get_notes, delete_note
from app.models import Note, NoteCreate


app = FastAPI(title="Notes API")


@app.post("/notes", response_model=Note)
def create(note: NoteCreate):
    return create_note(note)


@app.get("/notes", response_model=list[Note])
def list_notes():
    return get_notes()


@app.get("/notes/{note_id}", response_model=Note)
def get(note_id: int):
    note = get_note_by_id(note_id)
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@app.delete("/notes/{note_id}")
def delete(note_id: int):
    deleted = delete_note(note_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Note not found")
    return {"deleted": True}
