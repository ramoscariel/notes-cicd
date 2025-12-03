from pydantic import BaseModel


class NoteBase(BaseModel):
    title: str
    content: str


class Note(NoteBase):
    id: int


class NoteCreate(NoteBase):
    pass
