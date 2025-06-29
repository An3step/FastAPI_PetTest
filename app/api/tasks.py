from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..schemas.task import TaskCreate, TaskUpdate, TaskInDB
from ..crud import task as crud_task
from ..crud import analytics as crud_analytics

router = APIRouter()

@router.post("/", response_model=TaskInDB)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    # В реальном приложении здесь будет проверка авторизации
    user_id = 1  # временно, для примера
    return crud_task.create_task(db, task, user_id)

@router.get("/", response_model=List[TaskInDB])
def read_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_task.get_tasks(db, skip=skip, limit=limit)

@router.get("/{task_id}", response_model=TaskInDB)
def read_task(task_id: int, db: Session = Depends(get_db)):
    db_task = crud_task.get_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@router.put("/{task_id}", response_model=TaskInDB)
def update_task(task_id: int, task: TaskUpdate, db: Session = Depends(get_db)):
    db_task = crud_task.get_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return crud_task.update_task(db, task_id=task_id, task=task)

@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    if not crud_task.delete_task(db, task_id=task_id):
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted successfully"}

@router.post("/{task_id}/complete")
def complete_task(task_id: int, actual_time: int, db: Session = Depends(get_db)):
    db_task = crud_task.complete_task(db, task_id=task_id, actual_time=actual_time)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Обновляем аналитику
    crud_analytics.update_task_analytics(db, task_id=task_id, actual_time=actual_time)
    
    return {"message": "Task completed and analytics updated"}