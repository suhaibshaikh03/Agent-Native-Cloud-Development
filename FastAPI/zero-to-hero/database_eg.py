from sqlmodel import SQLModel,Field, create_engine
from fastapi import FastAPI
from typing import Optional, List
from pydantic import Field
from datetime import datetime
from dotenv import load_dotenv
import os
app = FastAPI()
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", echo=True)
engine = create_engine(DATABASE_URL)

class Task(SQLModel, table=True):
    """Task stored in database."""
    id: Optional[int] = Field(default=None, primary_key=True)
    description: Optional[str] = Field(min_length=1, max_length=200)
    title: str = Field(min_length=1, max_length=200)



@app.get("/getalltasks")
def get_tasks() -> List[Task]:
    pass

@app.get("/gettask/{task_id}")
def get_task(task_id: int) -> Task:
    pass

@app.post(f"/createtask")
def create_task(task: Task) -> Task:
    pass
