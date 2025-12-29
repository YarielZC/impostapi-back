from fastapi import APIRouter, Depends, status, HTTPException

from logic.jwt_auth_user import auth_user

from api.manage_routes.project_manage import delete_project

from models.project_model import ProjectResponse
from models.user_model import UserResponse
from repositories.project_repository import ProjectRepository, get_project_repository
from repositories.user_repository import UserRepository, get_user_repository

manage_user_router = APIRouter(prefix='/me',
                   tags=['Manage User'],
                   )
# async def delete_project(id: str, repo: ProjectRepository = Depends(get_project_repository), repoEndpoint: EndpointRepository = Depends(get_endpoint_repository), user: UserResponse = Depends(auth_user)):

@manage_user_router.get('/', response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_my_info(repo: UserRepository = Depends(get_user_repository), user: UserResponse = Depends(auth_user)):
  return user

@manage_user_router.delete('/delete', status_code=status.HTTP_204_NO_CONTENT)
async def delete_my_user(repo: UserRepository = Depends(get_user_repository), repoProject: ProjectRepository = Depends(get_project_repository), user: UserResponse = Depends(auth_user)):

  projects = await repoProject.find_all(user.id)

  if len(projects) != 0:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                        detail='User have projects yet')
  
  for project_id in user.project_shared:
    project = await repoProject.find_one_by_id(project_id)
    if not project:
      raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                          detail='Unknow error')
    project = ProjectResponse(**project)
    new_permissed_list = project.permissed.copy()
    try:
      new_permissed_list.remove(user.id)
      await repoProject.update_permissed_users(project.id, new_permissed_list)
    except:
      pass


  
  result = await repo.delete_user_by_id(user.id)

  if result != 1:
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail='Unknow error')
  
