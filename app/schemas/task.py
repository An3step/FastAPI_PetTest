from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum

class TaskPriority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"

class TaskStatus(str, Enum):
    backlog = "backlog"
    todo = "todo"
    in_progress = "in_progress"
    done = "done"
    archived = "archived"

class TaskBase(BaseModel):
    title: str = Field(..., max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    priority: TaskPriority = TaskPriority.medium
    status: TaskStatus = TaskStatus.todo
    due_date: Optional[datetime] = None
    estimated_time: Optional[int] = Field(None, gt=0, description="Time in minutes")

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    priority: Optional[TaskPriority] = None
    status: Optional[TaskStatus] = None
    due_date: Optional[datetime] = None
    estimated_time: Optional[int] = Field(None, gt=0)
    actual_time: Optional[int] = Field(None, gt=0)

class TaskInDB(TaskBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True