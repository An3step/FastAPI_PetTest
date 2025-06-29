from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class TaskAnalyticsBase(BaseModel):
    completion_count: int
    last_completed: Optional[datetime] = None
    average_completion_time: Optional[float] = None
    efficiency_ratio: Optional[float] = None

class TaskAnalyticsResponse(TaskAnalyticsBase):
    task_id: int
    
    class Config:
        from_attributes = True

class EfficiencyReport(BaseModel):
    date: str
    average_efficiency: float
    tasks_completed: int