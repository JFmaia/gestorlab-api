from typing import List
from fastapi import APIRouter, status, Depends, HTTPException
from datetime import datetime

from sqlalchemy.future import select
from sqlalchemy.orm import Session

from models.pending import Pending
from models.permissao import Permissao
from models.usuario import Usuario

from core.deps import get_session, get_current_user

from schemas.pending_schema import PendingSchema, PendingAccepted

router = APIRouter()

#GET User Pendentes all
@router.get('/', response_model= List[PendingSchema])
async def get_pending_all(db: Session = Depends(get_session)):
  query = select(Pending)
  result = db.execute(query)
  pendings: List[Pending] = result.scalars().unique().all()

  return pendings

#GET User Pendentes ativos
@router.get('/ativos', response_model= List[PendingSchema])
async def get_pending_ativos(db: Session = Depends(get_session)):
  query = select(Pending).filter(Pending.ativo == True)
  result = db.execute(query)
  pendings: List[Pending] = result.scalars().unique().all()

  return pendings

#POST User Pendentes
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=PendingSchema)
async def post_pending(
    pending: PendingSchema, 
    db: Session = Depends(get_session)
):
    query = select(Pending).filter(Pending.ativo == True).filter(Pending.matricula_user == pending.matricula_user)
    result = db.execute(query)
    veryUsuario: Pending = result.scalars().unique().one_or_none()

    if(veryUsuario):
        raise HTTPException(detail="Já existe um pedido desse usuario!", status_code=status.HTTP_403_FORBIDDEN)
    else:
        novo_pedido: Pending = Pending(
            id_user= pending.id_user,
            matricula_user = pending.matricula_user
        )
        db.add(novo_pedido)
        db.commit()
        return novo_pedido

#POST Aceitar user
@router.post('/pendingAccepted', status_code=status.HTTP_200_OK)
async def acceped_pending(
    pending: PendingAccepted, 
    usuario_logado: Usuario = Depends(get_current_user), 
    db: Session = Depends(get_session)
):
    query = select(Usuario).filter(Usuario.id == pending.id_user)
    result = db.execute(query)
    usuario: Usuario = result.scalars().unique().one_or_none()

    if(usuario == None):
        raise HTTPException(detail="O usuário informado não foi encontrado!", status_code=status.HTTP_404_NOT_FOUND)
    else:
        usuario.id_perm = pending.id_perm
        usuario.data_atualizacao = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        usuario.ativo = True
        db.commit()

    query = select(Pending).filter(Pending.id == pending.id)
    result = db.execute(query)
    pendingSearch: Pending = result.scalars().unique().one_or_none()

    if pendingSearch is None:
        raise HTTPException(detail="Nenhum pedido encontrado!", status_code=status.HTTP_404_NOT_FOUND)
    else:
        pendingSearch.ativo = False
        db.commit()

@router.delete('/deletePending/{id_peding}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_usuario(id_peding: str, db: Session = Depends(get_session), usuario_logado: Usuario = Depends(get_current_user)):
    query = select(Pending).filter(Pending.id == id_peding)
    result = db.execute(query)
    pedido: Pending = result.scalars().unique().one_or_none()

    if pedido is None:
        raise HTTPException(detail="Pedido não encontrado!", status_code=status.HTTP_404_NOT_FOUND)
    else:
        db.delete(pedido)
        db.commit()