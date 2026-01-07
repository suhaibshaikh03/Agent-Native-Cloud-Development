from sqlmodel import SQLModel,Field, create_engine, select, Session
from fastapi import FastAPI, Depends
from typing import Optional, List
from datetime import datetime
from dotenv import load_dotenv
import os
app = FastAPI()
load_dotenv()

DATABASE_URL = os.getenv("DB_URL")
engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session


class Task(SQLModel, table=True):
    """Task stored in database."""
    id: Optional[int] = Field(default=None, primary_key=True, nullable=False)
    description: Optional[str] = Field(min_length=1, max_length=200)
    title: str = Field(min_length=1, max_length=200)




@app.get("/getalltasks")
def get_tasks(session: Session = Depends(get_session)) -> List[Task]:
    tasks = session.exec(select(Task)).all()
    return tasks

@app.get("/gettask/{task_id}")
def get_task(task_id: int, session: Session = Depends(get_session)) -> Task:
    pass
    

@app.post(f"/createtask")
def create_task(task: Task, session: Session = Depends(get_session)) -> Task:
    session.add(task)
    session.commit()
    session.refresh(task)
    return task
    
