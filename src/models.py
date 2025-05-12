from datetime import datetime
from pydantic import BaseModel, Field


class EventBody(BaseModel):
    title: str = Field(..., min_length=1)


class Todo(BaseModel):
    id: str
    title: str
    done: bool
    created_at: datetime
