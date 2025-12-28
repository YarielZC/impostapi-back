from models.user_model import UserCreate
from repositories.user_repository import UserRepository
from fastapi import HTTPException, status

async def user_validation(user: UserCreate, repo: UserRepository):
  
  # Username is a unique key
  found = await repo.find_one_by_field('username', user.username)

  if found:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                        detail='That username already exists')
  
  # Email is a unique key
  found = await repo.find_one_by_field('email', user.email)

  if found:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                        detail='That email has already a account')
  

