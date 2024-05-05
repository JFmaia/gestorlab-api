from typing import List

from fastapi import APIRouter, status, Depends, HTTPException, Response

from sqlalchemy.future import  select

from models.laboratorio import Laboratorio
from models.usuario import Usuario
from schemas.laboratorio_schema import LaboratorioSchema, LaboratorioSchemaCreate, LaboratorioSchemaUp
from core.deps import get_session, get_current_user
from datetime import datetime

router = APIRouter()

#POST Laboratorio
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=LaboratorioSchema)
async def post_laboratorio(
    laboratorio: LaboratorioSchemaCreate, 
    usuario_logado: Usuario = Depends(get_current_user), 
    db= Depends(get_session)
):
    
    novo_laboratorio: Laboratorio = Laboratorio(
        coordenador_id= usuario_logado.id,
        nome = laboratorio.nome,
        sobre= laboratorio.sobre,
        template= laboratorio.template,
        descricao= laboratorio.descricao,
        email= laboratorio.email,
    )

    db.add(novo_laboratorio)
    db.commit()

    return novo_laboratorio

#GET Laboratorios
@router.get('/', response_model= List[LaboratorioSchema], status_code=status.HTTP_200_OK)
async def get_laboratorios(db= Depends(get_session)):
    with db as session:
        query = select(Laboratorio)
        result = session.execute(query)
        laboratorios: List[Laboratorio] = result.scalars().unique().all()

    return laboratorios

#GET laboratorio
@router.get('/{laboratorio_id}', response_model= LaboratorioSchema, status_code=status.HTTP_200_OK)
async def get_laboratorio(laboratorio_id: str, db= Depends(get_session)):
    with db as session:
        query = select(Laboratorio).filter(Laboratorio.id == laboratorio_id)
        result = session.execute(query)
        laboratorio: Laboratorio = result.scalars().unique().one_or_none()
    
    if laboratorio:
        return laboratorio
    else:
        raise HTTPException(detail="laboratorio não encontrado", status_code=status.HTTP_404_NOT_FOUND)

#PUT laboratorio
@router.put('/{laboratorio_id}', response_model=LaboratorioSchema, status_code=status.HTTP_202_ACCEPTED)
async def put_laboratorio(laboratorio_id: str, laboratorio: LaboratorioSchemaUp, db= Depends(get_session), usuario_logado: Usuario = Depends(get_current_user)):
    with db as session:
        query = select(Laboratorio).filter(Laboratorio.id == laboratorio_id)
        result = session.execute(query)
        laboratorio_up: Laboratorio = result.scalars().unique().one_or_none()
    
        if laboratorio_up:
            if laboratorio.nome:
                laboratorio_up.nome = laboratorio.nome
            if laboratorio.descricao:
                laboratorio_up.descricao = laboratorio.descricao
            if laboratorio.sobre:
                laboratorio_up.sobre = laboratorio.sobre
            if laboratorio.template:
                laboratorio_up.template = laboratorio.template
            if laboratorio.email:
                laboratorio_up.email= laboratorio.email
           
            laboratorio_up.data_up = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            session.add(laboratorio_up)
            session.commit()
            
            return laboratorio_up
        
        else:
            raise HTTPException(detail="laboratorio não encontrado!", status_code=status.HTTP_404_NOT_FOUND)
        
#DELETE laboratorio
@router.delete('/{laboratorio_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_laboratorio(laboratorio_id: str, db= Depends(get_session), usuario_logado: Usuario = Depends(get_current_user)):
    with db as session:
        query = select(Laboratorio).filter(Laboratorio.id == laboratorio_id).filter(Laboratorio.coordenador_id == usuario_logado.id)
        result = session.execute(query)
        laboratorio_del: Laboratorio = result.scalars().unique().one_or_none()
    
        if laboratorio_del:
           
            session.delete(laboratorio_del)
            session.commit()
            
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        
        else:
            raise HTTPException(detail="Laboratorio não encontrado!", status_code=status.HTTP_404_NOT_FOUND)
        
#DELETE laboratorio
@router.delete('/removeMember/{laboratorio_id}/{member_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_member_laboratory(laboratorio_id: str, member_id: str, db= Depends(get_session), usuario_logado: Usuario = Depends(get_current_user)):
    with db as session:
        query = select(Laboratorio).filter(Laboratorio.id == laboratorio_id).filter(Laboratorio.coordenador_id == usuario_logado.id)
        result = session.execute(query)
        laboratorio: Laboratorio = result.scalars().unique().one_or_none()

        for member in laboratorio.membros:
            if member.id == member_id:
                session.delete(member)
                session.commit()
                return Response(detail="Membro removido com sucesso!", status_code=status.HTTP_204_NO_CONTENT)
        
        else:
            raise HTTPException(detail="Membro não encontrado!", status_code=status.HTTP_404_NOT_FOUND)