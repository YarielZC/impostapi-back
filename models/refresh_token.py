from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

class RefreshToken(BaseModel):
  user_id: str
  token: str
  created_at: datetime = Field(default_factory=lambda: datetime.utcnow())

  model_config = ConfigDict(
    populate_by_name=True,
  )

class RefreshTokenResponse(RefreshToken):
  id: str = Field(alias='_id')
