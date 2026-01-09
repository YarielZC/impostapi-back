from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from passlib.context import CryptContext 

from core.settings import settings

from models.refresh_token import RefreshToken, RefreshTokenResponse
from models.user_model import UserDB, UserResponse, UserCreate

from repositories.refresh_token_repository import RefreshTokenRepository, get_refresh_token_repository
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
async def login(repo: UserRepository = Depends(get_user_repository), form: OAuth2PasswordRequestForm = Depends(), repoRefreshToken: RefreshTokenRepository = Depends(get_refresh_token_repository)):
  user = await repo.find_one_by_field('email', form.username)
  if not user:
    user = await repo.find_one_by_field('username', form.username)

  if not user:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                        detail='Username or password is wrong')
  
  userdb = UserDB(**user)
  user = UserResponse(**user)

  if not crypt.verify(form.password, userdb.password):
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                        detail='Username or password is wrong')
  
  access_token_expiration = datetime.utcnow() + timedelta(minutes=settings.TOKEN_DURATION)
  access_token = {
    'sub': userdb.username,
    'exp': access_token_expiration
  }

  refresh_token_expiration = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_DAY_DURATION)
  refresh_token = {
    'sub': userdb.username,
    'exp': refresh_token_expiration,
    'type': 'refresh'
  }

  refresh_token = jwt.encode(refresh_token,
                            key=settings.SECRET_TOKEN_KEY,
                            algorithm=settings.ALGORITHM_CRYPT)

  result = await repoRefreshToken.find_all(userdb.id)

  newResult = []

  for item in result:
    newItem = item
    newItem['_id'] = str(newItem['_id'])
    newResult.append(newItem)

  if result:
    for token in newResult:
      token_db = RefreshTokenResponse(**token)

      await repoRefreshToken.delete_by_id(token_db.id)

  newRefreshToken = RefreshToken(user_id=userdb.id,
                                 token=refresh_token)
  
  created_id = await repoRefreshToken.insert_one(newRefreshToken)
  result = await repoRefreshToken.find_one_by_id(created_id)

  if not result:
     HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                   detail='Error to login')

  
  return {
    'user': user.model_dump(),
    'access_token': jwt.encode(access_token,
                               key=settings.SECRET_TOKEN_KEY,
                               algorithm=settings.ALGORITHM_CRYPT),
    'refresh_token': refresh_token,
    'token_type': 'bearer'
  }

oauth2 = OAuth2PasswordBearer(tokenUrl='/auth/login')


@auth_router.get('/refresh_auth', response_model=dict, status_code=status.HTTP_200_OK)
async def refresh_auth(token: str = Depends(oauth2), repo: UserRepository = Depends(get_user_repository), repoRefreshToken: RefreshTokenRepository = Depends(get_refresh_token_repository)):
  unauthorized_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalide credentials",
                            headers={"WWW-Authenticate": 'Bearer'})
  
  try:
      user = jwt.decode(token, settings.SECRET_TOKEN_KEY, settings.ALGORITHM_CRYPT).get('sub')
      
  except:
      raise unauthorized_exception
  if not user:
      raise unauthorized_exception
  
  user_db = await repo.find_one_by_field('username', user)

  if not user_db:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='User not is registered')
                            
  
  user_db = UserDB(**user_db)

  result = await repoRefreshToken.find_one_by_field('token', token)

  if not result:
     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                         detail='You do not have acceses, invalid token')

  



  access_token_expiration = datetime.utcnow() + timedelta(minutes=settings.TOKEN_DURATION)
  access_token = {
    'sub': user_db.username,
    'exp': access_token_expiration
  }

  refresh_token_expiration = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_DAY_DURATION)
  refresh_token = {
    'sub': user_db.username,
    'exp': refresh_token_expiration,
    'type': 'refresh'
  }

  refresh_token = jwt.encode(refresh_token,
                            key=settings.SECRET_TOKEN_KEY,
                            algorithm=settings.ALGORITHM_CRYPT)

  result = await repoRefreshToken.find_all(user_db.id)

  newResult = []

  for item in result:
    newItem = item
    newItem['_id'] = str(newItem['_id'])
    newResult.append(newItem)

  if result:
     for token in newResult:
        token_db = RefreshTokenResponse(**token)  # type: ignore
        await repoRefreshToken.delete_by_id(token_db.id)

  newRefreshToken = RefreshToken(user_id=user_db.id,
                                 token=refresh_token)
  
  created_id = await repoRefreshToken.insert_one(newRefreshToken)
  result = await repoRefreshToken.find_one_by_id(created_id)

  if not result:
     HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                   detail='Error to login')


  return {
    'access_token': jwt.encode(access_token,
                               key=settings.SECRET_TOKEN_KEY,
                               algorithm=settings.ALGORITHM_CRYPT),
    'refresh_token': refresh_token,
    'token_type': 'bearer'
  }