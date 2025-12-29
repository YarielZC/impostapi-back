from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

class EndpointCreate(BaseModel):
  name: str
  description: str | None = None
  method: str
  path_url: str
  response: str | dict | None = None
  status_code: int
  delay: int | None = None
  is_public: bool
  project_id: str
  update_at: datetime = Field(default_factory=lambda: datetime.now())
  created_at: datetime = Field(default_factory=lambda: datetime.now())

class EndpointResponse(EndpointCreate):
  id: str = Field(alias='_id')

  model_config = ConfigDict(
    populate_by_name=True,
  )