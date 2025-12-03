import pytest
from app import crud
from app.models import NoteCreate


@pytest.fixture(autouse=True)
def reset_db():
    """Reset in-memory DB before each test."""
    crud.db.clear()
    crud.next_id = 1


def test_create_note():
    note_data = NoteCreate(title="Test Note", content="Hello World")
    note = crud.create_note(note_data)

    assert note.id == 1
    assert note.title == "Test Note"
    assert note.content == "Hello World"
    assert len(crud.db) == 1


def test_get_notes():
    crud.create_note(NoteCreate(title="N1", content="C1"))
    crud.create_note(NoteCreate(title="N2", content="C2"))

    notes = crud.get_notes()

    assert len(notes) == 2
    assert notes[0].title == "N1"
    assert notes[1].title == "N2"


def test_get_note_by_id_found():
    note = crud.create_note(NoteCreate(title="Find Me", content="Exists"))
    result = crud.get_note_by_id(note.id)

    assert result is not None
    assert result.id == note.id
    assert result.title == "Find Me"


def test_get_note_by_id_not_found():
    result = crud.get_note_by_id(999)
    assert result is None


def test_delete_note_success():
    note = crud.create_note(NoteCreate(title="Delete Me", content="Gone soon"))
    deleted = crud.delete_note(note.id)

    assert deleted is True
    assert len(crud.db) == 0


def test_delete_note_not_found():
    deleted = crud.delete_note(12345)
    assert deleted is False
