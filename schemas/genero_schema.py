from typing import Optional
from pydantic import BaseModel, UUID4

class GeneroSchema(BaseModel):
    id: Optional[UUID4] = None
    title: Optional[str]

    class Config:
        from_attributes = True