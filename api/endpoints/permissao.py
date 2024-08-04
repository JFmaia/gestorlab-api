from typing import List
from fastapi import APIRouter, status, Depends

from sqlalchemy.future import  select
from sqlalchemy.ext.asyncio import AsyncSession
from models.permissao import Permissao
from models.permissaoLab import PermissaoOfLab
from schemas.permissao_schema import PermissaoSchema
from core.deps import get_session, get_current_user

router = APIRouter()

#GET Permissões
@router.get('/', response_model= List[PermissaoSchema], status_code=status.HTTP_200_OK)
async def get_permissoes(db: AsyncSession = Depends(get_session)):
  query = select(Permissao)
  result = await db.execute(query)
  permissaos: List[Permissao] = result.scalars().unique().all()

  return permissaos

#GET Permissões
@router.get('/permLab', response_model= List[PermissaoSchema], status_code=status.HTTP_200_OK)
async def get_permissoes(db: AsyncSession = Depends(get_session)):
  query = select(PermissaoOfLab)
  result = await db.execute(query)
  permissaos: List[PermissaoOfLab] = result.scalars().unique().all()

  return permissaos