from pymongo.asynchronous.database import AsyncDatabase

from db.connection import get_database
from models.user_model import UserCreate, UserResponse
from .base_repository import BaseRepository

from fastapi import Depends

class UserRepository(BaseRepository):
  def __init__(self, database: AsyncDatabase) -> None:
    super().__init__(database, 'users')
    self.db = database[self.collection]

  async def update_password(self, id: str, newPassword: str):
    result = await self.db.update_one({'_id': self._to_object_id(id)},
                                      {
                                        '$set': {
                                          'password': newPassword
                                        }
                                      })
    return result.modified_count

  async def update_name(self, id: str, name: str):
    result = await self.db.update_one({'_id': self._to_object_id(id)}, 
                                      {
                                        '$set': {
                                          'name': name
                                        }
                                      })
    
    return result.modified_count

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
    result = await self.db.insert_one(user.model_dump())
    return result.inserted_id
    
  async def delete_user_by_id(self, id: str):
    result = await self.db.delete_one({'_id': self._to_object_id(id)})
    return result.deleted_count
  
  async def update_shared_projects(self, id: str, newSharedProjects: list[str]):
    result = await self.db.update_one({'_id': self._to_object_id(id)}, {
      '$set': {
        'project_shared': newSharedProjects
      }
    })
    return result

def get_user_repository(database: AsyncDatabase = Depends(get_database)):
  return UserRepository(database=database)