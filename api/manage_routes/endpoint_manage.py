from fastapi import APIRouter, HTTPException, status, Depends
from logic.jwt_auth_user import auth_user
from models.user_model import UserResponse
from repositories.endpoint_repository import get_endpoint_repository, EndpointRepository
from models.endpoint_model import EndpointResponse, EndpointCreate
from validations.endpoint_validation import endpoint_validation

manage_endpoint_router = APIRouter(prefix='/endpoint',
                   tags=['Manage Endpoint'],
                   )

@manage_endpoint_router.put('/update/{id}', status_code=status.HTTP_201_CREATED, response_model=EndpointResponse)
async def update_endpoint(newEndpoint: EndpointCreate, id: str, repo: EndpointRepository = Depends(get_endpoint_repository)):
  
  oldEndpoint = await repo.find_one_by_id(id)

  if not oldEndpoint:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail='Endpoint not founded')
  
  result = await repo.update_one_by_id(id, newEndpoint)
  if result != 0:

    return await repo.find_one_by_id(id)

  if result == 0:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail='Endpoint does not exist')
  
  raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                      detail='Unknow server error')

@manage_endpoint_router.delete('/delete/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_endpoint(id: str, repo: EndpointRepository = Depends(get_endpoint_repository)):
  result = await repo.delete_by_id(id)

  if result == 1:
    return

  if result == 0:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail='Endpoint does not exist')
  
  raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                      detail='Unknow server error')


@manage_endpoint_router.post('/create', response_model=EndpointResponse, status_code=status.HTTP_201_CREATED)
async def create_endpoint(endpoint: EndpointCreate, repo: EndpointRepository = Depends(get_endpoint_repository), user: UserResponse = Depends(auth_user)):
  
  await endpoint_validation(endpoint, repo)

  id_newed = await repo.insert_one(endpoint)  

  if not id_newed:
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                  detail='Endpoint was not created but it should')
    
  result = await repo.find_one_by_id(id=id_newed)

  if not result:
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail='Endpoint was not created but it should')
  
  return EndpointResponse(**result)