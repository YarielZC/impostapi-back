from fastapi import HTTPException, status

from models.project_model import ProjectResponse
from models.user_model import UserResponse
from repositories.project_repository import ProjectRepository


async def only_permissed_member_project(repoProject: ProjectRepository, project_id: str, user: UserResponse):
  project = await repoProject.find_one_by_id(project_id)

  if not project:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail='Project not founded')
  project = ProjectResponse(**project)
  project_permissed_list = project.permissed

  if not user.id in project_permissed_list:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                        detail='Forbidden')