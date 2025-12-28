from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
import jwt
from passlib.context import CryptContext 

from core.settings import settings

from models.user_model import UserDB, UserResponse, UserCreate

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
  
  return UserResponse(**new_user)

@auth_router.post('/login', response_model=dict, status_code=status.HTTP_202_ACCEPTED)
async def login(repo: UserRepository = Depends(get_user_repository), form: OAuth2PasswordRequestForm = Depends()):
  user = await repo.find_one_by_field('email', form.username)
  if not user:
    user = await repo.find_one_by_field('username', form.username)

  if not user:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                        detail='Username or password is wrong')
  
  user = UserDB(**user)

  if not crypt.verify(form.password, user.password):
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                        detail='Username or password is wrong')
  
  access_token_expiration = datetime.now() + timedelta(minutes=settings.TOKEN_DURATION)
  access_token = {
    'sub': user.username,
    'exp': access_token_expiration
  }

  return {
    'access_token': jwt.encode(access_token,
                               key=settings.SECRET_TOKEN_KEY,
                               algorithm=settings.ALGORITHM_CRYPT),
    'token_type': 'bearer'
  }
