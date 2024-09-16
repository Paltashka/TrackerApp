from typing import Optional, List
from pydantic import BaseModel
from app.features.task.models import Status, Priority


class TaskBase(BaseModel):
    title: str
    description: str
    assigned_developers_ids: List[int]
    status: Status
    priority: Priority


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[Status] = None
    priority: Optional[Priority] = None
    assigned_developers_ids: Optional[List[int]] = None


class UserInTask(BaseModel):
    username: str

    class Config:
        orm_mode = True


class TaskShow(BaseModel):
    title: str
    description: str
    responsible_person: Optional[UserInTask]
    assigned_developers: Optional[List[UserInTask]]
    status: Status
    priority: Priority

    class Config:
        orm_mode = True
