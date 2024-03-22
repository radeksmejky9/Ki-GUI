# main.py

from fastapi import FastAPI
import os
from database_init import initialize_database
from routers.project import project_router  # Import our new projet_router

ALLOWED_ORIGIN: list = (
    os.getenv("CORS_ALLOWED_ORIGIN", "http://localhost:8000")
    .replace(" ", "")
    .split(",")
)
ALLOWED_METHODS: list = (
    os.getenv("CORS_ALLOWED_METHODS", "GET, POST, PUT, DELETE, PATCH")
    .replace(" ", "")
    .split(",")
)
ALLOWED_HEADERS: list = (
    os.getenv("CORS_ALLOWED_HEADERS", "*").replace(" ", "").split(",")
)
ALLOW_CREDENTIALS: bool = os.getenv("CORS_ALLOW_CREDENTIALS", "TRUE") == "TRUE"
MAX_AGE: int = int(os.getenv("CORS_MAX_AGE", 600))


app = FastAPI()
app.include_router(project_router)  # register out new project_router


@app.get("/")
def root():
    return {"message": "Hello World"}


initialize_database()
