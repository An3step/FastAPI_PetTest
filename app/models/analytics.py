from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base
from datetime import datetime

class TaskAnalytics(Base):
    __tablename__ = "task_analytics"
    
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id"))
    completion_count = Column(Integer, default=0)
    last_completed = Column(DateTime)
    average_completion_time = Column(Float)  # в минутах
    efficiency_ratio = Column(Float)  # estimated_time / actual_time
    
    task = relationship("Task", back_populates="analytics")
    
    def update_analytics(self, actual_time: int):
        """Обновляем аналитику после завершения задачи"""
        self.completion_count += 1
        self.last_completed = datetime.utcnow()
        
        # Обновляем среднее время выполнения
        if self.average_completion_time:
            self.average_completion_time = (
                self.average_completion_time * (self.completion_count - 1) + actual_time
            ) / self.completion_count
        else:
            self.average_completion_time = actual_time
            
        # Рассчитываем эффективность
        if self.task.estimated_time and actual_time > 0:
            self.efficiency_ratio = self.task.estimated_time / actual_time