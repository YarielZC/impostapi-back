from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

class UserBase(BaseModel):
  name: str
  username: str
  email: str

class UserCreate(UserBase):
  password: str

class UserResponse(UserBase):
  id: str = Field(alias='_id')
  created_at: datetime

  model_config = ConfigDict(
    populate_by_name=True,
  )