from fastapi import FastAPI, HTTPException
from app.crud import create_note, get_note_by_id, get_notes, delete_note
from app.models import Note, NoteCreate
from app.launchdarkly_config import get_feature_flag, close_launchdarkly


app = FastAPI(title="Notes API")


@app.on_event("shutdown")
def shutdown_event():
    close_launchdarkly()


@app.post("/notes", response_model=Note)
def create(note: NoteCreate):
    return create_note(note)


@app.get("/notes", response_model=list[Note])
def list_notes():
    # Feature flag: habilitar filtrado mejorado de notas
    enhanced_filtering = get_feature_flag("enhanced-note-filtering", "user-1", False)

    notes = get_notes()

    if enhanced_filtering:
        # Ordenar notas por ID descendente cuando el flag está activo
        notes = sorted(notes, key=lambda x: x.id, reverse=True)

    return notes


@app.get("/notes/{note_id}", response_model=Note)
def get(note_id: int):
    note = get_note_by_id(note_id)
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@app.delete("/notes/{note_id}")
def delete(note_id: int):
    # Feature flag: habilitar confirmación extendida en eliminación
    extended_delete_response = get_feature_flag("extended-delete-response", "user-1", False)

    deleted = delete_note(note_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Note not found")

    if extended_delete_response:
        return {
            "deleted": True,
            "note_id": note_id,
            "message": "Note successfully deleted"
        }

    return {"deleted": True}


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "notes-api",
        "feature_flags": {
            "enhanced-note-filtering": get_feature_flag("enhanced-note-filtering", "user-1", False),
            "extended-delete-response": get_feature_flag("extended-delete-response", "user-1", False)
        }
    }
