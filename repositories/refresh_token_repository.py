from fastapi import Depends
from db.connection import get_database
from models.refresh_token import RefreshToken
from repositories.base_repository import BaseRepository
from pymongo.asynchronous.database import AsyncDatabase

class RefreshTokenRepository(BaseRepository):
  def __init__(self, database: AsyncDatabase) -> None:
    super().__init__(database, 'refresh_tokens')
    self.db = database[self.collection]

  async def find_one_by_advance_method(self, conditions: dict):
    result = await self.db.find_one(conditions)

    try:
      result = self._map_doc(result)
    except:
      return None
    
    return result

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
  
  async def insert_one(self, endpoint: RefreshToken):
    result = await self.db.insert_one(endpoint.model_dump())
    return result.inserted_id
    
  async def delete_by_id(self, id: str):
    result = await self.db.delete_one({'_id': self._to_object_id(id)})
    return result.deleted_count
  
  async def find_all(self, user_id: str):
    result = self.db.find({'user_id': user_id})
    return await result.to_list()

def get_refresh_token_repository(database: AsyncDatabase = Depends(get_database)):
  return RefreshTokenRepository(database=database)