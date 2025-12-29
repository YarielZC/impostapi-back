from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
import jwt
from core.settings import settings
from models.user_model import UserResponse
from repositories.user_repository import UserRepository, get_user_repository


oauth2 = OAuth2PasswordBearer(tokenUrl='/auth/login')

async def auth_user(token: str = Depends(oauth2), repo: UserRepository = Depends(get_user_repository)):

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

    user_db = UserResponse(**user_db)

    return user_db