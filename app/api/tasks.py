from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
import math

from app.core.database import get_db
from app.services.task_service import TaskService
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse, TaskList

router = APIRouter(prefix="/tasks", tags=["tasks"])


def get_task_service(db: Session = Depends(get_db)) -> TaskService:
    return TaskService(db)


@router.post("/", response_model=TaskResponse, status_code=201)
async def create_task(
    task_data: TaskCreate,
    task_service: TaskService = Depends(get_task_service)
):
    """Create a new task"""
    return task_service.create_task(task_data)


@router.get("/", response_model=TaskList)
async def get_tasks(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(10, ge=1, le=100, description="Page size"),
    completed: Optional[bool] = Query(None, description="Filter by completion status"),
    task_service: TaskService = Depends(get_task_service)
):
    """Get tasks with pagination and filtering"""
    skip = (page - 1) * size
    tasks, total = task_service.get_tasks(skip=skip, limit=size, completed=completed)
    
    return TaskList(
        tasks=tasks,
        total=total,
        page=page,
        size=size,
        pages=math.ceil(total / size) if total > 0 else 1
    )


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int,
    task_service: TaskService = Depends(get_task_service)
):
    """Get a specific task"""
    task = task_service.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    task_data: TaskUpdate,
    task_service: TaskService = Depends(get_task_service)
):
    """Update a task"""
    task = task_service.update_task(task_id, task_data)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.delete("/{task_id}", status_code=204)
async def delete_task(
    task_id: int,
    task_service: TaskService = Depends(get_task_service)
):
    """Delete a task"""
    if not task_service.delete_task(task_id):
        raise HTTPException(status_code=404, detail="Task not found")


@router.patch("/{task_id}/complete", response_model=TaskResponse)
async def mark_task_completed(
    task_id: int,
    task_service: TaskService = Depends(get_task_service)
):
    """Mark a task as completed"""
    task = task_service.mark_completed(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.patch("/{task_id}/incomplete", response_model=TaskResponse)
async def mark_task_incomplete(
    task_id: int,
    task_service: TaskService = Depends(get_task_service)
):
    """Mark a task as incomplete"""
    task = task_service.mark_incomplete(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task
