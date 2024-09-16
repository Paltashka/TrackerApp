from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from app.core.database import get_db
from app.features.task.models import Task
from app.features.task.schemas import TaskBase, TaskUpdate, TaskShow
from app.features.user.models import User
from app.core.auth import get_current_user
from app.features.user.models import UserRole
from app.core.email import send_email

router = APIRouter(
    prefix="/task",
    tags=['Tasks']
)


@router.post("/create", response_model=TaskShow)
def create_task(task: TaskBase, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != UserRole.MANAGER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only managers can create tasks")

    assigned_developers = task.assigned_developers_ids

    new_task = Task(
        title=task.title,
        description=task.description,
        responsible_person_id=current_user.id,
        status=task.status,
        priority=task.priority
    )

    new_task.assigned_developers = db.query(User).filter(User.id.in_(assigned_developers)).all()

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task


@router.get("/all", response_model=List[TaskShow])
def get_all_tasks(db: Session = Depends(get_db),
                  current_user: User = Depends(get_current_user)):
    tasks = db.query(Task).options(joinedload(Task.assigned_developers)).all()
    return tasks


@router.get("/{task_id}", response_model=TaskShow)
def read_task(task_id: int, db: Session = Depends(get_db),
              current_user: User = Depends(get_current_user)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task


@router.put("/update/{task_id}", response_model=TaskShow)
def update_task(task_id: int, task: TaskUpdate, db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    if current_user.role == UserRole.MANAGER:
        for key, value in task.dict(exclude_unset=True).items():
            if key == "assigned_developers_ids":
                assigned_developers = db.query(User).filter(User.id.in_(value)).all()
                db_task.assigned_developers = assigned_developers
            else:
                setattr(db_task, key, value)

        db.commit()
        db.refresh(db_task)

    elif current_user.role == UserRole.USER and current_user in db_task.assigned_developers:
        if "status" in task.dict(exclude_unset=True):
            db_task.status = task.status
            db.commit()
            db.refresh(db_task)
            responsible_user = db.query(User).filter(User.id == db_task.responsible_person_id).first()
            if responsible_user:
                send_email(
                    to_email=responsible_user.email,
                    subject="Task Status Updated",
                    body=f"Hello, the status of your task '{db_task.title}' has been updated to '{db_task.status}'."
                )
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="You do not have permission to update this task")

    return db_task


@router.delete("/delete/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != UserRole.MANAGER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only managers can delete tasks")

    db_task = db.query(Task).filter(Task.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    db.delete(db_task)
    db.commit()
    return {"message": "Task deleted successfully"}
