from fastapi import APIRouter, HTTPException, status, Depends
from passlib.context import CryptContext 

from models.user_model import UserResponse, UserCreate

from repositories.user_repository import UserRepository, get_user_repository

from validations.user_validation import user_validation

crypt = CryptContext(schemes=['bcrypt'])

auth_router = APIRouter(prefix='/auth',
                   tags=['Authentication'],
                   )

@auth_router.post('/register_user', response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate, repo: UserRepository = Depends(get_user_repository)):

  await user_validation(user, repo)

  user_dict = user.model_dump()

  user_dict['password'] = crypt.hash(user_dict['password'])

  id = await repo.insert_one(UserCreate(**user_dict))

  new_user = await repo.find_one_by_id(id)

  if not new_user:
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail='User not created but it should')
  
  return new_user

