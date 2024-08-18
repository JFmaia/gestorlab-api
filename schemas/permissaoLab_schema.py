from typing import Optional
from pydantic import BaseModel, UUID4, ConfigDict

class PermissaoSchema(BaseModel):
  id: Optional[UUID4] = None 
  title: str
  
  model_config = ConfigDict(
    from_attributes=True
  )