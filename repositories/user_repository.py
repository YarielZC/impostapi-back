from pymongo.asynchronous.database import AsyncDatabase

from db.connection import get_database
from models.user_model import UserCreate, UserResponse
from .base_repository import BaseRepository

from fastapi import Depends

class UserRepository(BaseRepository):
  def __init__(self, database: AsyncDatabase) -> None:
    super().__init__(database, 'users')
    self.db = database[self.collection]

  async def find_one_by_field(self, field: str, value):
    result = await self.db.find_one({field: value})

    try:
      result = self._map_doc(result)
    except:
      return None
    
    return result
  
  async def find_one_by_id(self, id: str):
    result = await self.db.find_one({'_id': self._to_object_id(id)})

    try:
      result = self._map_doc(result)
    except:
      return None

    return result

  
  async def insert_one(self, user: UserCreate):
    result = await self.db.insert_one(dict(user))
    return result.inserted_id
    
  async def delete_user_by_id(self, id: str):
    result = await self.db.delete_one({'_id': id})
    return result.deleted_count

def get_user_repository(database: AsyncDatabase = Depends(get_database)):
  return UserRepository(database=database)