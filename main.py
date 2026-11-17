from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI("заметки")


class NoteCreate(BaseModel):
    title: str
    content: str

class NoteResponse(BaseModel):
    id: int

notes = []
note_id = 1

@app.post("/notes", response_model=NoteResponse)
def create_note(note: NoteCreate):
    global note_id
    new_note = NoteResponse(id=note_id, **note.model_dump())
    notes.append(new_note)
    note_id += 1
    return new_note

@app.get("/notes/", response_model=list[NoteResponse])
def read_notes():
    return notes

@app.get("/notes/{note_id}", response_model=NoteResponse)
def read_note(note_id: int):
    for note in notes:
        if note.id == note_id:
            return note
    return {"error": "Заметка не найдена"}

@app.delete("/notes/{note_id}")
def delete_note(note_id: int):
    global notes
    notes = [note for note in notes if note.id != note_id]
    return {"message": "Заметка удалена"}