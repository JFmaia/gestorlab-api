from typing import Optional
from pydantic import BaseModel, UUID4

class PermissaoSchema(BaseModel):
  id: Optional[UUID4] = None 
  title: str
    
  class Config:
    from_attributes = True