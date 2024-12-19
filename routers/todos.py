from fastapi import APIRouter, Depends, HTTPException, Path
from pydantic import BaseModel, Field
from database import session_local
from typing import Annotated
from sqlalchemy.orm import Session
from models import Todos, Base
from starlette import status

router = APIRouter()

def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority:int = Field(gt=0, lt=6)
    complete:bool

@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(db:db_dependency):
    return db.query(Todos).all()

@router.get("/{id}")
async def read_by_id(db:db_dependency, id:Annotated[int, Path(gt=0)]):
    todo =  db.query(Todos).filter(Todos.id == id).first()
    if todo is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return todo

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_todo(db:db_dependency, todo_request: TodoRequest):
    todo_model = Todos(**todo_request.model_dump())
    db.add(todo_model)
    db.commit()

@router.put("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(db:db_dependency, todo_request:TodoRequest, id:int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail='Item not found.')
    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete
    db.add(todo_model)
    db.commit()

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(db:db_dependency, id:int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail='Item not found.')
    db.query(Todos).filter(Todos.id == id).delete()
    db.commit()