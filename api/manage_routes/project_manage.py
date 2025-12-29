from fastapi import APIRouter, HTTPException, status, Depends
from logic.jwt_auth_user import auth_user
from models.project_model import ProjectCreate, ProjectResponse
from models.user_model import UserResponse
from repositories.project_repository import ProjectRepository, get_project_repository
from repositories.endpoint_repository import EndpointRepository, get_endpoint_repository
from logic.owner_project import owner_project_validate

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

@manage_project_router.delete('/delete/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(id: str, repo: ProjectRepository = Depends(get_project_repository), repoEndpoint: EndpointRepository = Depends(get_endpoint_repository), user: UserResponse = Depends(auth_user)):

  await owner_project_validate(project_id=id,
                               repo=repo,
                               user=user)
  
  result = await repoEndpoint.delete_many({'project_id': id})
  result = await repo.delete_by_id(id)

  if result != 1:
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail='Unknow error')

@manage_project_router.get('/count_endpoints/{id}', response_model=int, status_code=status.HTTP_200_OK)
async def count_endpoints(id: str, repo: ProjectRepository = Depends(get_project_repository), repoEndpoint: EndpointRepository = Depends(get_endpoint_repository), user: UserResponse = Depends(auth_user)):
  
  await owner_project_validate(project_id=id,
                               repo=repo,
                               user=user)
  
  result = await repoEndpoint.count_endpoints(id)
  return len(await result.to_list())
   

