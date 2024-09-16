import enum
from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship, Session
from app.core.database import Base
from app.features.task.models import task_users


class UserRole(enum.Enum):
    ADMIN = "admin"
    USER = "user"
    MANAGER = "manager"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String)
    password = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.USER)

    responsible_tasks = relationship(
        'Task',
        foreign_keys='Task.responsible_person_id',
        back_populates='responsible_person'
    )

    tasks = relationship('Task', secondary=task_users, back_populates='assigned_developers')

    @classmethod
    def get_by_id(cls, db: Session, user_id: int):
        return db.query(cls).filter(cls.id == user_id).first()

