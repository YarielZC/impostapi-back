from models.endpoint_model import EndpointCreate
from repositories.endpoint_repository import EndpointRepository
from repositories.project_repository import ProjectRepository
from fastapi import HTTPException, status


async def endpoint_validation(endpoint: EndpointCreate, repo: EndpointRepository, repoProject: ProjectRepository):
  
  found = await repo.find_one_by_advance_method({'project_id': endpoint.project_id, 
                                                 'path_url': endpoint.path_url,
                                                 'method': endpoint.method})

  if found:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f'The url: {endpoint.path_url} with method: {endpoint.method}, already exist in this project')
  
  if endpoint.status_code == 204 and endpoint.response != None:
    raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                        detail='Satus code 204 not accept response body, it must be None')

  foundProject = await repoProject.find_one_by_id(endpoint.project_id)

  if not foundProject:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                        detail='Incorrect project')