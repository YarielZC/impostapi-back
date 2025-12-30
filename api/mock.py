import asyncio
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse

from repositories.endpoint_repository import EndpointRepository, get_endpoint_repository
from models.endpoint_model import EndpointResponse

mock_router = APIRouter(prefix='/mock',
                   tags=['Mocks'],
                   )

@mock_router.api_route('/{user:str}/{project:str}/{fullpath:path}', methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
async def m(request: Request, user: str, project: str, fullpath: str, repo: EndpointRepository = Depends(get_endpoint_repository)):
  
  method = request.method.lower()

  endpoint = await repo.find_one_by_advance_method({'path_url': fullpath,
                                                    'method': method})
  # print(fullpath)
  if not endpoint:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f'Endpoint: {fullpath} not founded with method: {method}')
  endpoint = EndpointResponse(**endpoint)

  if endpoint.delay:
      await asyncio.sleep(endpoint.delay / 1000)  
      
  if endpoint.status_code == 204:
    return
  return JSONResponse(endpoint.response,
                      status_code=endpoint.status_code)