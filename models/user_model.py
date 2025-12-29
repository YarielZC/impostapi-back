from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, field_validator

class UserBase(BaseModel):
  name: str = Field(min_length=1)
  username: str = Field(min_length=3)
  email: str
  project_shared: list[str] = []
  created_at: datetime = Field(default_factory=lambda: datetime.now())

  @field_validator('username', mode='before')
  @classmethod
  def validate_username(cls, username: str):
    return username.lower()


class UserCreate(UserBase):
  password: str
class UserResponse(UserBase):
  id: str = Field(alias='_id')

  model_config = ConfigDict(
    populate_by_name=True,
  )

class UserDB(UserCreate, UserResponse):
  pass