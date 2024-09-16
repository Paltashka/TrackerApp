from sqlalchemy import Column, Integer, String, Enum, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.core.database import Base
from enum import Enum as PyEnum


class Status(PyEnum):
    TODO = "TODO"
    IN_PROGRESS = "In progress"
    DONE = "Done"


class Priority(PyEnum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


task_users = Table(
    'task_users', Base.metadata,
    Column('task_id', Integer, ForeignKey('tasks.id')),
    Column('user_id', Integer, ForeignKey('users.id'))
)

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    responsible_person_id = Column(Integer, ForeignKey('users.id'))
    status = Column(Enum(Status), default=Status.TODO)
    priority = Column(Enum(Priority), default=Priority.LOW)

    responsible_person = relationship('User', foreign_keys=[responsible_person_id])
    assigned_developers = relationship('User', secondary=task_users, back_populates='tasks')
