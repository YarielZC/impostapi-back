from pydantic import BaseModel, ConfigDict, Field, model_validator
from datetime import datetime

class ProjectBase(BaseModel):
  name: str
  description: str | None = None
class ProjectCreate(ProjectBase):
  
  permissed: list[str] = []
  owner_id: str | None = None
  create_at: datetime = Field(default_factory=lambda: datetime.now())

  @model_validator(mode='after')
  def set_default_permissed_list(self):
    if not self.owner_id:
      return self
    if self.permissed == []:
      self.permissed = [self.owner_id]
    return self

class ProjectUpdate(BaseModel):
  name: str | None = None
  description: str | None = None
class ProjectResponse(ProjectCreate):
  id: str = Field(alias='_id')

  model_config = ConfigDict(
    populate_by_name=True,
  )