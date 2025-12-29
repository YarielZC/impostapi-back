from fastapi import APIRouter, HTTPException, status, Depends
from logic.jwt_auth_user import auth_user
from models.user_model import UserResponse
from repositories.endpoint_repository import get_endpoint_repository, EndpointRepository
from models.endpoint_model import EndpointResponse, EndpointCreate
from validations.endpoint_validation import endpoint_validation

manage_endpoint_router = APIRouter(prefix='/endpoint',
                   tags=['Manage Endpoint'],
                   )

@manage_endpoint_router.post('/create_endpoint', response_model=EndpointResponse, status_code=status.HTTP_201_CREATED)
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