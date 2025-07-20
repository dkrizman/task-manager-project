from sqlalchemy.orm import Session
from typing import List, Optional
import math
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate


class TaskService:
    def __init__(self, db: Session):
        self.db = db

    def create_task(self, task_data: TaskCreate) -> Task:
        """Create a new task"""
        db_task = Task(**task_data.model_dump())
        self.db.add(db_task)
        self.db.commit()
        self.db.refresh(db_task)
        return db_task

    def get_task(self, task_id: int) -> Optional[Task]:
        """Get a task by ID"""
        return self.db.query(Task).filter(Task.id == task_id).first()

    def get_tasks(self, skip: int = 0, limit: int = 10, completed: Optional[bool] = None) -> tuple[List[Task], int]:
        """Get tasks with pagination and filtering"""
        query = self.db.query(Task)
        
        if completed is not None:
            query = query.filter(Task.completed == completed)
        
        total = query.count()
        tasks = query.offset(skip).limit(limit).all()
        
        return tasks, total

    def update_task(self, task_id: int, task_data: TaskUpdate) -> Optional[Task]:
        """Update a task"""
        db_task = self.get_task(task_id)
        if not db_task:
            return None
        
        update_data = task_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_task, field, value)
        
        self.db.commit()
        self.db.refresh(db_task)
        return db_task

    def delete_task(self, task_id: int) -> bool:
        """Delete a task"""
        db_task = self.get_task(task_id)
        if not db_task:
            return False
        
        self.db.delete(db_task)
        self.db.commit()
        return True

    def mark_completed(self, task_id: int) -> Optional[Task]:
        """Mark a task as completed"""
        return self.update_task(task_id, TaskUpdate(completed=True))

    def mark_incomplete(self, task_id: int) -> Optional[Task]:
        """Mark a task as incomplete"""
        return self.update_task(task_id, TaskUpdate(completed=False))