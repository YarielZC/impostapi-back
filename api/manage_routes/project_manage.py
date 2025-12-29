from fastapi import APIRouter, HTTPException, status, Depends
from logic.jwt_auth_user import auth_user
from models.project_model import ProjectCreate, ProjectResponse
from models.user_model import UserResponse
from repositories.project_repository import ProjectRepository, get_project_repository

manage_project_router = APIRouter(prefix='/project',
                   tags=['Manage Project'],
                   )

@manage_project_router.post('/create', response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(project: ProjectCreate, repo: ProjectRepository = Depends(get_project_repository), user: UserResponse = Depends(auth_user)):
  
  newProject = project
  newProject.owner_id = user.id
  
  result = await repo.insert_one(project)
  
  if not result:
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                  detail='Unknow error')
    
  result = await repo.find_one_by_id(result)

  if not result:
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                  detail='Unknow error')

  return ProjectResponse(**result)