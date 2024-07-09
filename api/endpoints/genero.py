from typing import List
from fastapi import APIRouter, status, Depends

from sqlalchemy.future import  select
from sqlalchemy.orm import Session
from models.genero import Genero
from schemas.genero_schema import GeneroSchema
from core.deps import get_session, get_current_user

router = APIRouter()

#GET Permissões
@router.get('/', response_model= List[GeneroSchema], status_code=status.HTTP_200_OK)
async def get_generos(db: Session = Depends(get_session)):
  query = select(Genero)
  result = db.execute(query)
  generos: List[Genero] = result.scalars().unique().all()

  return generos