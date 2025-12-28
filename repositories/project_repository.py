from pymongo.asynchronous.database import AsyncDatabase

from models.project_model import ProjectCreate
from .base_repository import BaseRepository


class ProjectRepository(BaseRepository):
  def __init__(self, database: AsyncDatabase) -> None:
    super().__init__(database, 'projects')
    self.db = database[self.collection]

  async def find_one_by_field(self, field: str, value):
    return await self.db.find_one({field: value})
  
  async def find_one_by_id(self, id: str):
    return await self.db.find_one({'_id': self._to_object_id(id)})
  
  async def insert_one(self, user: ProjectCreate):
    result = await self.db.insert_one(dict(user))
    return result.inserted_id
    
  async def delete_by_id(self, id: str):
    result = await self.db.delete_one({'_id': id})
    return result.deleted_count