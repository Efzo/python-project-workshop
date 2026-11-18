from itertools import count
from threading import Lock
from typing import Annotated

from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel, StringConstraints


Title = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=80)]


class NoteInput(BaseModel):
    title: Title
    body: str = ""


class Note(NoteInput):
    id: int


def create_app():
    app = FastAPI(title="Notes API")
    notes: dict[int, Note] = {}
    ids = count(1)
    lock = Lock()

    @app.post("/notes", response_model=Note, status_code=status.HTTP_201_CREATED)
    def create_note(data: NoteInput):
        with lock:
            note = Note(id=next(ids), **data.model_dump())
            notes[note.id] = note
            return note

    @app.get("/notes", response_model=list[Note])
    def list_notes():
        with lock:
            return list(notes.values())

    @app.get("/notes/{note_id}", response_model=Note)
    def get_note(note_id: int):
        with lock:
            if note_id not in notes:
                raise HTTPException(status_code=404, detail="Note not found")
            return notes[note_id]

    @app.put("/notes/{note_id}", response_model=Note)
    def replace_note(note_id: int, data: NoteInput):
        with lock:
            if note_id not in notes:
                raise HTTPException(status_code=404, detail="Note not found")
            notes[note_id] = Note(id=note_id, **data.model_dump())
            return notes[note_id]

    @app.delete("/notes/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
    def delete_note(note_id: int):
        with lock:
            if note_id not in notes:
                raise HTTPException(status_code=404, detail="Note not found")
            del notes[note_id]
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    return app


app = create_app()
