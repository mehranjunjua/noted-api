from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from dependencies import get_db
from models import Note as NoteModel


app = FastAPI()


class Note(BaseModel):
    title: str


class NoteResponse(BaseModel):
    id: int
    title: str


@app.get("/notes", response_model=list[NoteResponse])
def get_notes(db: Session = Depends(get_db)):
    return db.query(NoteModel).all()


@app.get("/notes/{id}", response_model=NoteResponse)
def get_note(id: int, db: Session = Depends(get_db)):
    note = db.query(NoteModel).filter(NoteModel.id == id).first()

    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")

    return note


@app.post("/notes")
def post_notes(note: Note, db: Session = Depends(get_db)):
    new_note = NoteModel(title=note.title)

    db.add(new_note)
    db.commit()
    db.refresh(new_note)

    return new_note


@app.put("/notes/{id}")
def put_notes(id: int, note: Note, db: Session = Depends(get_db)):
    existing_note = db.query(NoteModel).filter(NoteModel.id == id).first()

    if existing_note is None:
        raise HTTPException(status_code=404, detail="Note not found")

    existing_note.title = note.title

    db.commit()
    db.refresh(existing_note)

    return existing_note


@app.delete("/notes/{id}")
def delete_notes(id: int, db: Session = Depends(get_db)):
    existing_note = db.query(NoteModel).filter(NoteModel.id == id).first()

    if existing_note is None:
        raise HTTPException(status_code=404, detail="Note not found")

    db.delete(existing_note)
    db.commit()

    return existing_note