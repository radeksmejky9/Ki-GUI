# services/project_service.py

from fastapi import HTTPException
from sqlmodel import Session
from models import Project
from schemas.project import ProjectCreate
from database import commit_and_handle_exception, refresh_and_handle_exception


class ProjectService:

    def insert_project_db(self, project_create: ProjectCreate, session: Session):
        new_project = Project(
            name=project_create.name.strip(),
            description=project_create.description.strip(),
        )
        session.add(new_project)
        commit_and_handle_exception(session)
        refresh_and_handle_exception(session, new_project)
        return new_project

    def select_project_by_id_db(self, project_id: int, session: Session):
        project = self._get_project_by_id(project_id, session)
        return project

    def _get_project_by_id(self, project_id: int, session: Session):
        project = session.get(Project, project_id)
        if project is None:
            raise HTTPException(status_code=404, detail="Project not found")
        return project
