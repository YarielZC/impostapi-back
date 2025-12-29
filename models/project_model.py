from pydantic import BaseModel, ConfigDict, Field, model_validator
from datetime import datetime

class ProjectCreate(BaseModel):
  name: str
  description: str | None = None
  permissed: list[str] = []
  owner_id: str | None = None
  update_at: datetime = Field(default_factory=lambda: datetime.now())
  create_at: datetime = Field(default_factory=lambda: datetime.now())

  @model_validator(mode='after')
  def set_default_permissed_list(self):
    if not self.owner_id:
      return self
    self.permissed = [self.owner_id]
    return self

class ProjectResponse(ProjectCreate):
  id: str = Field(alias='_id')

  model_config = ConfigDict(
    populate_by_name=True,
  )