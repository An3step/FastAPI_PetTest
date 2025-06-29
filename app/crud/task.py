from sqlalchemy.orm import Session
from ..models.task import Task, TaskStatus
from ..schemas.task import TaskCreate, TaskUpdate
from datetime import datetime

def get_task(db: Session, task_id: int):
    return db.query(Task).filter(Task.id == task_id).first()

def get_tasks(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Task).offset(skip).limit(limit).all()

def create_task(db: Session, task: TaskCreate, user_id: int):
    db_task = Task(**task.model_dump(), user_id=user_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def update_task(db: Session, task_id: int, task: TaskUpdate):
    db_task = get_task(db, task_id)
    if not db_task:
        return None
    
    update_data = task.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_task, field, value)
    
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def delete_task(db: Session, task_id: int):
    db_task = get_task(db, task_id)
    if not db_task:
        return False
    
    db.delete(db_task)
    db.commit()
    return True

def complete_task(db: Session, task_id: int, actual_time: int):
    db_task = get_task(db, task_id)
    if not db_task:
        return None
    
    db_task.status = TaskStatus.done
    db_task.actual_time = actual_time
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task