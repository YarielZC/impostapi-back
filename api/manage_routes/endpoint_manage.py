from fastapi import APIRouter, HTTPException, status, Depends
from logic.jwt_auth_user import auth_user
from models.user_model import UserResponse
from repositories.endpoint_repository import get_endpoint_repository, EndpointRepository
from repositories.project_repository import get_project_repository, ProjectRepository
from repositories.user_repository import get_user_repository, UserRepository
from models.endpoint_model import EndpointResponse, EndpointCreate, EndpointUpdate
from models.project_model import ProjectResponse
from validations.endpoint_validation import endpoint_validation
from logic.permissed_member_project import only_permissed_member_project

manage_endpoint_router = APIRouter(prefix='/endpoint',
                   tags=['Manage Endpoint'],
                   )

@manage_endpoint_router.put('/update/{id}', status_code=status.HTTP_201_CREATED, response_model=EndpointResponse)
async def update_endpoint(newEndpoint: EndpointUpdate, id: str, repo: EndpointRepository = Depends(get_endpoint_repository), repoProject: ProjectRepository = Depends(get_project_repository), repoUser: UserRepository = Depends(get_user_repository), user: UserResponse = Depends(auth_user)):
  
  oldEndpoint = await repo.find_one_by_id(id)

  if not oldEndpoint:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail='Endpoint not founded')
  
  await only_permissed_member_project(repoProject=repoProject,
                                project_id=oldEndpoint['project_id'],
                                user=user)
  
  if newEndpoint.delay and newEndpoint.delay > 5000:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                        detail='Endpoint delay`s cannot be greater than 5000ms')

  endToCreate = EndpointCreate(**newEndpoint.model_dump(), project_id=oldEndpoint['project_id'])
  result = await repo.update_one_by_id(id, endToCreate)

  if result != 0:

    return await repo.find_one_by_id(id)

  else:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail='Endpoint does not exist')
  


@manage_endpoint_router.delete('/delete/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_endpoint(id: str, repo: EndpointRepository = Depends(get_endpoint_repository), repoProject: ProjectRepository = Depends(get_project_repository), user: UserResponse = Depends(auth_user)):
  oldEndpoint = await repo.find_one_by_id(id)
  if not oldEndpoint:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail='Endpoint not founded')
  
  await only_permissed_member_project(repoProject=repoProject,
                                project_id=oldEndpoint['project_id'],
                                user=user)

  result = await repo.delete_by_id(id)

  if result == 1:
    return

  if result == 0:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail='Endpoint does not exist')
  
  raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                      detail='Unknow server error')


@manage_endpoint_router.post('/create', response_model=EndpointResponse, status_code=status.HTTP_201_CREATED)
async def create_endpoint(endpoint: EndpointCreate, repo: EndpointRepository = Depends(get_endpoint_repository), repoProject: ProjectRepository = Depends(get_project_repository), user: UserResponse = Depends(auth_user)):
  
  await only_permissed_member_project(repoProject=repoProject,
                                project_id=endpoint.project_id,
                                user=user)
  
  if endpoint.delay and endpoint.delay > 5000:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                        detail='Endpoint delay`s cannot be greater than 5000ms')

  await endpoint_validation(endpoint, repo, repoProject)
  
  id_newed = await repo.insert_one(endpoint)  

  if not id_newed:
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                  detail='Endpoint was not created but it should')
    
  result = await repo.find_one_by_id(id=id_newed)

  if not result:
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail='Endpoint was not created but it should')
  
  return EndpointResponse(**result)