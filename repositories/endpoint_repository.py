from fastapi import Depends
from pymongo.asynchronous.database import AsyncDatabase

from db.connection import get_database
from models.endpoint_model import EndpointCreate
from .base_repository import BaseRepository


class EndpointRepository(BaseRepository):
  def __init__(self, database: AsyncDatabase) -> None:
    super().__init__(database, 'endpoints')
    self.db = database[self.collection]

  
  async def update_one_by_id(self, id: str, endpoint: EndpointCreate):
    result = await self.db.replace_one({'_id': self._to_object_id(id)}, endpoint.model_dump())
    return result

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
  
  async def insert_one(self, endpoint: EndpointCreate):
    result = await self.db.insert_one(endpoint.model_dump())
    return result.inserted_id
    
  async def delete_by_id(self, id: str):
    result = await self.db.delete_one({'_id': self._to_object_id(id)})
    return result.deleted_count
  
  async def delete_many(self, condition: dict):
    result = await self.db.delete_many(condition)
    return result.deleted_count
  
  async def count_endpoints(self, project_id: str):
    result = self.db.find({'project_id': project_id})
    return result


  
def get_endpoint_repository(database: AsyncDatabase = Depends(get_database)):
  return EndpointRepository(database=database)