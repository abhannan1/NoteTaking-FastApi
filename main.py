from fastapi import FastAPI, Depends, Query, Body, status, HTTPException
from fastapi.responses import JSONResponse
import uvicorn
from sqlalchemy.exc import  SQLAlchemyError, OperationalError
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from db import engine
from crud import CRUD
from typing import Annotated, List
from schemas import NoteModel, NoteCreateModel
import uuid
from models import Note
import time

app: FastAPI = FastAPI(
    title="Note API", description="This is a simple note taking service", docs_url="/"
)

session = async_sessionmaker(bind=engine, expire_on_commit=False)


db_ops = CRUD()

async def get_db():
    max_attempts = 3
    attempts = 0
    delay_time = 2

    db = session()
    
    while attempts < max_attempts :
        try:
            yield db
            break
        except OperationalError as e:
            print(f"failed to connect: {e}, retrying...")
            attempts += 1 
            time.sleep(delay_time)
        except SQLAlchemyError as e:
            print(f"exception occured: {e}")
        finally:
            await db.close()

        if max_attempts == attempts:
            print("failed to connect after multiple attempts")


bad_request = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Could not Procced with the request",
)

@app.exception_handler(SQLAlchemyError)
async def handle_database_errors(request, exc):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"message": "Database error"},
    )



@app.get("/notes",  response_model=List[NoteModel])
async def get_all_notes(db: Annotated[AsyncSession, Depends(get_db)])->Note:

    try:
        notes = await db_ops.get_all_notes(db)
    except HTTPException:
        raise bad_request
    return notes


@app.get("/notes/id", status_code=status.HTTP_200_OK)
async def get_note_by_id(db: Annotated[AsyncSession, Depends(get_db)], note_id: str):
        
    try:
        print(note_id, type(note_id))
        note = await db_ops.get_by_id(db, note_id)
        if not note:
            raise bad_request
    except SQLAlchemyError as e:
        print(f"error {e}")
        raise 
    return note


@app.post("/notes/add", status_code=status.HTTP_201_CREATED)
async def add_note(db: Annotated[AsyncSession, Depends(get_db)], note_data:NoteCreateModel = Body(embed=True)):
    try:
        new_note = Note(
         id=str(uuid.uuid4()),
         title=note_data.title,
         content= note_data.content
    )

        note = await db_ops.add(db, new_note)

    except HTTPException:
         raise bad_request
    return f"notes added : {note}"


@app.patch("/notes/update", status_code=status.HTTP_200_OK)
async def update_note(db: Annotated[AsyncSession, Depends(get_db)], note_id:str , note_data:NoteCreateModel = Body(embed=True)):
    try:
        note = await db_ops.update(db, note_id, data={"title":note_data.title, "content": note_data.content})
    except HTTPException:
         raise bad_request

    return note

@app.delete("/notes/delete", status_code=status.HTTP_200_OK)
async def delete_note(db: Annotated[AsyncSession, Depends(get_db)],note_id: str = Query(None)):
    try:
        note = await db_ops.get_by_id(db, note_id)
        result = await db_ops.delete(db,note )
    except HTTPException:
         raise bad_request

    return f"notes Deleted successfully {result}"


if __name__ == "__main__":
    uvicorn.run("main:app", log_level="info", reload=True, host="localhost", port=8000)
