from fastapi import Depends
from pymongo.asynchronous.database import AsyncDatabase

from db.connection import get_database
from models.project_model import ProjectCreate
from .base_repository import BaseRepository


class ProjectRepository(BaseRepository):
  def __init__(self, database: AsyncDatabase) -> None:
    super().__init__(database, 'projects')
    self.db = database[self.collection]

  async def update_name_and_description(self, id: str, name: str | None, description: str | None):
    if name and description:
      result = await self.db.update_one({'_id': self._to_object_id(id)}, {
                                         '$set': {
                                           'description': description,
                                           'name': name
                                         }})
    elif name:
      result = await self.db.update_one({'_id': self._to_object_id(id)}, {
                                         '$set': {
                                           'name': name
                                         }})
    elif description:
      result = await self.db.update_one({'_id': self._to_object_id(id)}, {
                                         '$set': {
                                           'description': description
                                         }})
    else:
      return -1
    return result.modified_count

  async def find_one_by_advance_method(self, conditions: dict):
    result = await self.db.find_one(conditions)

    try:
      result = self._map_doc(result)
    except:
      return None
    
    return result

  async def find_one_by_field(self, field: str, value):
    return await self.db.find_one({field: value})
  
  async def find_one_by_id(self, id: str):
    result = await self.db.find_one({'_id': self._to_object_id(id)})

    try:
      result = self._map_doc(result)
    except:
      return None
    return result

  async def insert_one(self, project: ProjectCreate):
    result = await self.db.insert_one(project.model_dump())
    return result.inserted_id
    
  async def delete_by_id(self, id: str):
    result = await self.db.delete_one({'_id': self._to_object_id(id)})
    return result.deleted_count
  
  async def find_all(self, user_id: str):
    result = self.db.find({'owner_id': user_id})
    return await result.to_list()
  
  async def update_permissed_users(self, id: str, newPermissedUsers: list[str]):
    result = await self.db.update_one({'_id': self._to_object_id(id)}, {
      '$set': {
        'permissed': newPermissedUsers
      }
    })
    return result
  
  async def add_request_count(self, id: str):
    result = await self.db.update_one({'_id': self._to_object_id(id)}, {
      '$inc': {'request_count': 1}
    })
    return result
  
def get_project_repository(database: AsyncDatabase = Depends(get_database)):
  return ProjectRepository(database=database)