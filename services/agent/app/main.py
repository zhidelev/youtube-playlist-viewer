from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .data import router
from .database import engine
from .models import Base

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(router)
