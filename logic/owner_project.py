from fastapi import HTTPException, status

from repositories.project_repository import ProjectRepository
from models.project_model import ProjectResponse
from models.user_model import UserResponse

async def owner_project_validate(project_id: str, repo: ProjectRepository, user: UserResponse):
  project = await repo.find_one_by_id(project_id)

  if not project:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail='Project not found')
  
  project = ProjectResponse(**project)
  
  if user.id != project.owner_id:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                        detail='You do not have permission to do this action')
  
  return project