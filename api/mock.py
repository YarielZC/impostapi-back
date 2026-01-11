import asyncio
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse

from models.project_model import ProjectResponse
from repositories.endpoint_repository import EndpointRepository, get_endpoint_repository
from repositories.project_repository import ProjectRepository, get_project_repository
from models.endpoint_model import EndpointResponse

mock_router = APIRouter(prefix='/mock',
                   tags=['Mocks'],
                   )

@mock_router.api_route('/{fullpath:path}', methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
async def m(request: Request, fullpath: str, repo: EndpointRepository = Depends(get_endpoint_repository), repoProject: ProjectRepository = Depends(get_project_repository)):
  
  method = request.method.lower()

  endpoint = await repo.find_one_by_advance_method({'path_url': fullpath,
                                                    'method': method})
  print(fullpath)
  if not endpoint:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f'Endpoint: {fullpath} not founded with method: {method}')
  
  endpoint = EndpointResponse(**endpoint)

  result = await repoProject.add_request_count(endpoint.project_id)
  print(endpoint.project_id)
  if result.modified_count == 0:
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail='Error to update the request count')

  if endpoint.delay:
      await asyncio.sleep(endpoint.delay / 1000)  
      
  if endpoint.status_code == 204:
    return
  return JSONResponse(endpoint.response,
                      status_code=endpoint.status_code)