from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

class EndpointBase(BaseModel):
  name: str
  description: str | None = None
  method: str
  path_url: str
  response: str | dict | None = None
  status_code: int
  delay: int | None = None
class EndpointCreate(EndpointBase):
  
  project_id: str
  update_at: datetime = Field(default_factory=lambda: datetime.now())
  created_at: datetime = Field(default_factory=lambda: datetime.now())

  def change_url(self, url: str):
    self.path_url = url

class EndpointUpdate(EndpointBase):
  pass
class EndpointResponse(EndpointCreate):
  id: str = Field(alias='_id')

  model_config = ConfigDict(
    populate_by_name=True,
  )