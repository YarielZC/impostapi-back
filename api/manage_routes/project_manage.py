from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from logic.jwt_auth_user import auth_user
from models.endpoint_model import EndpointResponse
from models.project_model import ProjectCreate, ProjectResponse
from models.user_model import UserResponse
from repositories.user_repository import UserRepository, get_user_repository
from repositories.project_repository import ProjectRepository, get_project_repository
from repositories.endpoint_repository import EndpointRepository, get_endpoint_repository
from logic.owner_project import owner_project_validate
from logic.permissed_member_project import only_permissed_member_project
##QUE UN USUARIO NO PUEDA CON LA ID DE UN PROYECTO ASIGNARLE UN ENDPOINT A UN PROYECTO QUE NO ES EL DE EL
manage_project_router = APIRouter(prefix='/project',
                   tags=['Manage Project'],
                   )

@manage_project_router.post('/create', response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(project: ProjectCreate, repo: ProjectRepository = Depends(get_project_repository), user: UserResponse = Depends(auth_user)):
  
  newProject = project
  newProject.owner_id = user.id
  if not newProject.owner_id:
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail='Owner id not founded')
  
  newProject.permissed.append(newProject.owner_id)

  
  result = await repo.insert_one(newProject)
  
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
  
  result = await repoEndpoint.find_all(id)
  return len(result)
   
@manage_project_router.get('/endpoints/{id}', response_model=list[EndpointResponse], status_code=status.HTTP_200_OK)
async def get_all_endpoints(id: str, repo: ProjectRepository = Depends(get_project_repository), repoEndpoint: EndpointRepository = Depends(get_endpoint_repository), user: UserResponse = Depends(auth_user)):

  await only_permissed_member_project(repoProject=repo,
                                      project_id=id,
                                      user=user)
  
  result = await repoEndpoint.find_all(id)

  newResult = []

  for item in result:
    newItem = item
    newItem['_id'] = str(newItem['_id'])
    newResult.append(newItem)

  return newResult

@manage_project_router.get('/projects', response_model=list[ProjectResponse], status_code=status.HTTP_200_OK)
async def get_all_projects(repo: ProjectRepository = Depends(get_project_repository), repoUser: UserRepository = Depends(get_user_repository), user: UserResponse = Depends(auth_user)):
  result = await repo.find_all(user.id)
  newResult = []

  for item in result:
    newItem = item
    newItem['_id'] = str(newItem['_id'])
    newResult.append(newItem)
  
  for project in user.project_shared:
    resultProject = await repo.find_one_by_id(project)

    if not resultProject:
      oldProjectList = user.project_shared.copy()
      oldProjectList.remove(project)
      await repoUser.update_shared_projects(user.id, oldProjectList)

    else:
      newResult.append(ProjectResponse(**resultProject))

  return newResult

@manage_project_router.post('/share/{project_id:str}/{user_id:str}', response_model=dict, status_code=status.HTTP_202_ACCEPTED)
async def share_project(project_id: str, user_id: str, repo: ProjectRepository = Depends(get_project_repository), repoUser: UserRepository = Depends(get_user_repository), user: UserResponse = Depends(auth_user)):
  
  project = await owner_project_validate(project_id=project_id,
                         repo=repo,
                         user=user)

  if user_id in project.permissed:
    return JSONResponse(content={'message': 'this user is already into this project'})

  user_to_share = await repoUser.find_one_by_id(user_id)
  
  if not user_to_share:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail='User not founded')

  user_to_share = UserResponse(**user_to_share)
  try:
    if user_to_share.project_shared.index(project_id) != -1:
      return JSONResponse(content={'message': 'this user is already into this project'})
  except:
    pass

  user_to_share.project_shared.append(project.id)

  result = await repoUser.update_shared_projects(user_to_share.id, user_to_share.project_shared)
  if result.modified_count == 0:
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail='Unknow error')
  try:
    if project.permissed.index(user_id) != -1:
      return JSONResponse(content={'message': 'this user is already into this project'})
  except:
    pass

  newPermissedUsers = project.permissed.copy()
  newPermissedUsers.append(user_id)
  
  result = await repo.update_permissed_users(project_id, newPermissedUsers)

  if result.modified_count == 0:
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail='Unknow error')
  
  return JSONResponse(content={'message': 'Project shared'})

@manage_project_router.delete('/share/{project_id:str}/{user_id:str}', response_model=dict, status_code=status.HTTP_202_ACCEPTED)
async def delete_share(project_id: str, user_id: str, repo: ProjectRepository = Depends(get_project_repository), repoUser: UserRepository = Depends(get_user_repository), user: UserResponse = Depends(auth_user)):
  
  project = await owner_project_validate(project_id=project_id,
                                         repo=repo,
                                         user=user)
  
  if user_id in project.permissed:
    new_permissed = project.permissed.copy()
    try:
      new_permissed.remove(user_id)
      result = await repo.update_permissed_users(project_id, new_permissed)
    except:
      pass
  
  user_search = await repoUser.find_one_by_id(user_id)

  if not user_search:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail='User not founded')
  
  user_search = UserResponse(**user_search)

  new_project_shared = user_search.project_shared.copy()
  try:
    new_project_shared.remove(project_id)
    result = await repoUser.update_shared_projects(user_id, new_project_shared)
  except:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                        detail='Project was not shared with the user')
  
  return JSONResponse(content={'message': 'Project unshare'})

