from typing import List
from fastapi import APIRouter, status, Depends

from sqlalchemy.future import  select
from sqlalchemy.orm import Session

from models.permissao import Permissao
from models.permissaoLab import PermissaoOfLab

from schemas.permissao_schema import PermissaoSchema

from core.deps import get_session

router = APIRouter()

#GET Permissões
@router.get('/', response_model= List[PermissaoSchema], status_code=status.HTTP_200_OK)
async def get_permissoes(db: Session = Depends(get_session)):
  query = select(Permissao)
  result = db.execute(query)
  permissaos: List[Permissao] = result.scalars().unique().all()

  return permissaos

#GET Permissões
@router.get('/permLab', response_model= List[PermissaoSchema], status_code=status.HTTP_200_OK)
async def get_permissoes(db: Session = Depends(get_session)):
  query = select(PermissaoOfLab)
  result = db.execute(query)
  permissaos: List[PermissaoOfLab] = result.scalars().unique().all()

  return permissaos