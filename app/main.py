from fastapi import FastAPI
from app.features.user.models import Base
from app.core.database import engine
from app.features.user.routes import router as user_router
from app.features.task.routes import router as task_router
from app.features.user.authentication import router as authentication_router

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(authentication_router)
app.include_router(user_router)
app.include_router(task_router)
