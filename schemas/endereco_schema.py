from typing import Optional
from datetime import datetime
from pydantic import BaseModel, UUID4, ConfigDict

class EnderecoSchema(BaseModel):
  id: Optional[UUID4] = None
  logradouro: str
  numero:int
  complemento:str
  bairro:str
  cidade:str
  estado:str
  cep:int
  pais:str
  data_inicial:Optional[datetime] = None
  data_up:Optional[datetime] = None

  model_config = ConfigDict(
    from_attributes=True
  )