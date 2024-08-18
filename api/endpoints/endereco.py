from typing import List
from fastapi import APIRouter, status, Depends, HTTPException

from sqlalchemy.future import  select
from sqlalchemy.orm import Session

from models.endereco import Endereco
from models.usuario import Usuario

from core.deps import get_current_user

from schemas.endereco_schema import EnderecoSchema

from core.deps import get_session

from datetime import datetime

router = APIRouter()

#GET Endereco
@router.get('/', response_model= List[EnderecoSchema], status_code=status.HTTP_200_OK)
async def get_enderecos(db: Session = Depends(get_session)):
  query = select(Endereco)
  result = db.execute(query)
  enderecos: List[Endereco] = result.scalars().unique().all()

  return enderecos

#Put Endereco
@router.put('/{id}', response_model= EnderecoSchema, status_code=status.HTTP_200_OK)
async def update_endereco(id:str, endereco: EnderecoSchema, db: Session = Depends(get_session), usuario_logado: Usuario = Depends(get_current_user)):
  if usuario_logado:
        query = select(Endereco).filter(Endereco.id == id)
        result = db.execute(query)
        endereco_up: Endereco = result.scalars().unique().one_or_none()

        if endereco_up:
            if endereco.logradouro:
                endereco_up.logradouro = endereco.logradouro
            if endereco.numero:
                endereco_up.numero = endereco.numero
            if endereco.bairro:
                endereco_up.bairro = endereco.bairro
            if endereco.cidade:
                endereco_up.cidade = endereco.cidade
            if endereco.estado:
                endereco_up.estado= endereco.estado
            if endereco.complemento:
                endereco_up.complemento = endereco.complemento
            if endereco.cep:
                endereco_up.cep = endereco.cep
            if endereco.pais:
                endereco_up.pais = endereco.pais

            endereco_up.data_up = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            db.commit()
            
            return endereco_up
        
        else:
            raise HTTPException(detail="Endereço não encontrado!", status_code=status.HTTP_404_NOT_FOUND)
        

#Put Endereco
@router.delete('/{id}', status_code=status.HTTP_202_ACCEPTED)
async def delete_endereco(id:str, db: Session = Depends(get_session), usuario_logado: Usuario = Depends(get_current_user)):
    query = select(Endereco).filter(Endereco.id == id)
    result = db.execute(query)
    endereco: Endereco = result.scalars().unique().one_or_none()

    if endereco is None:
        raise HTTPException(detail="Endereço não encontrado!", status_code=status.HTTP_404_NOT_FOUND)
    else:
        db.delete(endereco)
        db.commit()