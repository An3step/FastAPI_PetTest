from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..schemas.analytics import TaskAnalyticsResponse, EfficiencyReport
from ..crud import analytics as crud_analytics

router = APIRouter()

@router.get("/task/{task_id}", response_model=TaskAnalyticsResponse)
def get_task_analytics(task_id: int, db: Session = Depends(get_db)):
    analytics = crud_analytics.get_task_analytics(db, task_id=task_id)
    if not analytics:
        raise HTTPException(status_code=404, detail="Analytics not found for this task")
    return analytics

@router.get("/efficiency-report/", response_model=List[EfficiencyReport])
def get_efficiency_report(days: int = 7, db: Session = Depends(get_db)):
    report_data = crud_analytics.get_efficiency_report(db, days=days)
    return [
        EfficiencyReport(
            date=row.date,
            average_efficiency=row.avg_efficiency,
            tasks_completed=row.tasks_completed
        )
        for row in report_data
    ]