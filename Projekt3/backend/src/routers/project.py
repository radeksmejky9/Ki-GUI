# routers/project.py

from typing import Annotated
from fastapi import APIRouter, Depends
from services.project_service import ProjectService
from schemas.project import ProjectRead, ProjectCreate
from database import get_session
from sqlmodel import Session


project_router = APIRouter(prefix="/project", tags=["Project"])

db_dependency = Annotated[Session, Depends(get_session)]

project_service = ProjectService()


@project_router.post("/", response_model=ProjectRead)
def create_project(project_create: ProjectCreate, session: db_dependency):
    """
    ## Create a new project

    This endpoint will create a new project in the database.

    - **project_create**: Project object

    Returns:
    - `project`: Project object
    """
    new_project = project_service.insert_project_db(project_create, session)
    return ProjectRead.from_project(new_project)


@project_router.get("/{project_id}", response_model=ProjectRead)
def read_project(project_id: int, session: db_dependency):
    """
    ## Retrieve a project from the database

    This endpoint will return a project based on the ID passed on provided project_id.

    - **project_id**: ID of the project to retrieve

    Returns:
    - `project`: Project object
    """
    project = project_service.select_project_by_id_db(project_id, session)
    return ProjectRead.from_project(project)


@project_router.get("/", response_model=list[ProjectRead])
def read_all_projects(session: db_dependency):
    """
    ## Retrieve all projects from the database

    This endpoint will return all projects in the database.

    Returns:
    - `projects`: List of project objects
    """
    projects = project_service.select_all_projects_db(session)
    return [ProjectRead.from_project(project) for project in projects]
