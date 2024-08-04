from typing import List
from fastapi import APIRouter, status, Depends, HTTPException
from datetime import datetime

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.pending import Pending
from models.permissao import Permissao
from models.usuario import Usuario

from core.deps import get_session, get_current_user

from schemas.pending_schema import PendingSchema, PendingAccepted

router = APIRouter()

#GET User Pendentes
@router.get('/', response_model= List[PendingSchema])
async def get_pending(db: AsyncSession = Depends(get_session)):
  query = select(Pending).filter(Pending.ativo == True)
  result = await db.execute(query)
  pendings: List[Pending] = result.scalars().unique().all()

  return pendings

#POST User Pendentes
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=PendingSchema)
async def post_pending(
    pending: PendingSchema, 
    db: AsyncSession = Depends(get_session)
):
    novo_pedido: Pending = Pending(
        id_user= pending.id_user,
        matricula_user = pending.matricula_user
    )

    query = select(Pending).filter(Pending.matricula_user == pending.matricula_user)
    result = await db.execute(query)
    veryUsuario: Usuario = result.scalars().unique().one_or_none()

    if(veryUsuario):
        raise HTTPException(detail="Já existe um pedido desse usuario!", status_code=status.HTTP_403_FORBIDDEN)
    else:
        db.add(novo_pedido)
        await db.commit()
        return novo_pedido

#POST Aceitar user
@router.post('/pendingAccepted', status_code=status.HTTP_200_OK)
async def post_projeto(
    pending: PendingAccepted, 
    usuario_logado: Usuario = Depends(get_current_user), 
    db: AsyncSession = Depends(get_session)
):
    list_aux: List[Permissao] = []
    query = select(Usuario).filter(Usuario.id == pending.id_user)
    result = await db.execute(query)
    usuario: Usuario = result.scalars().unique().one_or_none()

    if(usuario == None):
        raise HTTPException(detail="Nenhum usuário encontrado", status_code=status.HTTP_404_NOT_FOUND)
    else:
      if pending.list_permissoes:
        query= select(Permissao)
        result= await db.execute(query)
        permissoes: List[Permissao] = result.scalars().unique().all()

        for item in pending.list_permissoes:
            for permissao in permissoes:
                if item == permissao.id:
                    list_aux.append(permissao)
        usuario.permissoes.clear()
        usuario.permissoes = list_aux
        usuario.data_atualizacao = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        usuario.ativo = True
        await db.commit()

    query = select(Pending).filter(Pending.id == pending.id)
    result = await db.execute(query)
    pendingSearch: Pending = result.scalars().unique().one_or_none()

    if(pendingSearch == None):
        raise HTTPException(detail="Nenhum pedido encontrado!", status_code=status.HTTP_404_NOT_FOUND)
    else:
        pendingSearch.ativo = False
        await db.commit()