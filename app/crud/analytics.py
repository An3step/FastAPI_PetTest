from sqlalchemy.orm import Session
from ..models.analytics import TaskAnalytics
from ..models.task import Task

def get_task_analytics(db: Session, task_id: int):
    return db.query(TaskAnalytics).filter(TaskAnalytics.task_id == task_id).first()

def create_task_analytics(db: Session, task_id: int):
    db_analytics = TaskAnalytics(task_id=task_id)
    db.add(db_analytics)
    db.commit()
    db.refresh(db_analytics)
    return db_analytics

def update_task_analytics(db: Session, task_id: int, actual_time: int):
    db_analytics = get_task_analytics(db, task_id)
    if not db_analytics:
        db_analytics = create_task_analytics(db, task_id)
    
    db_analytics.update_analytics(actual_time)
    db.add(db_analytics)
    db.commit()
    db.refresh(db_analytics)
    return db_analytics

def get_efficiency_report(db: Session, days: int = 7):
    # Здесь можно добавить сложные SQL-запросы для аналитики
    # Это пример простой реализации
    from datetime import datetime, timedelta
    from sqlalchemy import func
    
    date_threshold = datetime.utcnow() - timedelta(days=days)
    
    result = db.query(
        func.date(TaskAnalytics.last_completed).label("date"),
        func.avg(TaskAnalytics.efficiency_ratio).label("avg_efficiency"),
        func.count(TaskAnalytics.id).label("tasks_completed")
    ).filter(
        TaskAnalytics.last_completed >= date_threshold
    ).group_by(
        func.date(TaskAnalytics.last_completed)
    ).all()
    
    return result