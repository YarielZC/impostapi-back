from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime

class ProjectCreate(BaseModel):
  name: str
  description: str | None = None
  is_public: bool = False

class ProjectResponse(ProjectCreate):
  id: str = Field(alias='_id')
  owner_id: str
  update_at: datetime = Field(default_factory=lambda: datetime.now())
  create_at: datetime = Field(default_factory=lambda: datetime.now())

  model_config = ConfigDict(
    populate_by_name=True,
  )