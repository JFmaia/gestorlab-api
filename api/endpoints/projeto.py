from typing import List

from fastapi import APIRouter, status, Depends, HTTPException, Response

from sqlalchemy.future import  select

from sqlalchemy.orm import Session

from models.projeto import Projeto
from models.usuario import Usuario
from schemas.projeto_schema import ProjetoSchema,ProjetoSchemaCreate,ProjetoSchemaUp, ProjetoSchemaAddMember
from core.deps import get_session, get_current_user
from datetime import datetime

router = APIRouter()

#POST Projeto
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=ProjetoSchema)
async def post_projeto(
    projeto: ProjetoSchemaCreate, 
    usuario_logado: Usuario = Depends(get_current_user), 
    db: Session = Depends(get_session)
):
    novo_projeto: Projeto = Projeto(
        autor_id= usuario_logado.id,
        titulo = projeto.titulo,
        descricao= projeto.descricao,
        lab_creator= projeto.labCreator
    )

    query = select(Projeto).filter(Projeto.titulo == novo_projeto.titulo)
    result = db.execute(query)
    veryfProjeto: Projeto = result.scalars().unique().one_or_none()

    if(veryfProjeto):
        raise HTTPException(detail="Já existe um projeto com esse nome!!", status_code=status.HTTP_403_FORBIDDEN)
    else:
        db.add(novo_projeto)
        db.commit()
        return novo_projeto

#GET Projetos
@router.get('/', response_model= List[ProjetoSchema], status_code=status.HTTP_200_OK)
async def get_projetos(db: Session = Depends(get_session)):
   
    query = select(Projeto)
    result = db.execute(query)
    projetos: List[Projeto] = result.scalars().unique().all()

    return projetos

#GET Projeto
@router.get('/{projeto_id}', response_model= ProjetoSchema, status_code=status.HTTP_200_OK)
async def get_projeto(projeto_id: str, db: Session = Depends(get_session)):
   
    query = select(Projeto).filter(Projeto.id == projeto_id)
    result = db.execute(query)
    projeto: Projeto = result.scalars().unique().one_or_none()
    
    if projeto:
        return projeto
    else:
        raise HTTPException(detail="Projeto não encontrado", status_code=status.HTTP_404_NOT_FOUND)

#PUT Projeto
@router.put('/{projeto_id}', response_model=ProjetoSchema, status_code=status.HTTP_202_ACCEPTED)
async def put_projeto(projeto_id: str, projeto: ProjetoSchemaUp, db: Session = Depends(get_session), usuario_logado: Usuario = Depends(get_current_user)):
    query = select(Projeto).filter(Projeto.id == projeto_id)
    result = db.execute(query)
    projeto_up: Projeto = result.scalars().unique().one_or_none()

    if projeto_up:
        if projeto.titulo:
            projeto_up.titulo = projeto.titulo
        if projeto.descricao:
            projeto_up.descricao = projeto.descricao
            
        projeto_up.data_up = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        db.commit()
        return projeto_up
    
    else:
        raise HTTPException(detail="Projeto não encontrado!", status_code=status.HTTP_404_NOT_FOUND)
        
#DELETE Projeto
@router.delete('/{projeto_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_projeto(projeto_id: str, db: Session = Depends(get_session), usuario_logado: Usuario = Depends(get_current_user)):
    query = select(Projeto).filter(Projeto.id == projeto_id)
    result = db.execute(query)
    projeto_del: Projeto = result.scalars().unique().one_or_none()

    if projeto_del:
        if(projeto_del.autor_id == usuario_logado.id):
            db.delete(projeto_del)
            db.commit()
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail="Você não tem permissão para excluir este projeto!", status_code=status.HTTP_403_FORBIDDEN)
    
    else:
        raise HTTPException(detail="Projeto não encontrado!", status_code=status.HTTP_404_NOT_FOUND)

##POST member in laboratory
@router.post('/addMember/{projeto_id}/{usuario_id}', status_code=status.HTTP_201_CREATED)
async def post_member(projeto_id: str , usuario_id: str , db: Session = Depends(get_session), usuario_logado: Usuario = Depends(get_current_user)): 
   
    query = select(Projeto).filter(Projeto.id == projeto_id).filter(Projeto.coordenador_id == usuario_logado.id)
    result = db.execute(query)
    projeto:Projeto = result.scalars().unique().one_or_none()

    if projeto is None:
        raise HTTPException(detail="Projeto não encontrado!", status_code=status.HTTP_404_NOT_FOUND)

    query = select(Usuario).filter(Usuario.id == usuario_id)
    result = db.execute(query)
    usuario: Usuario = result.scalars().unique().one_or_none()

    if usuario is None:
        raise HTTPException(detail="Usuario não encontrado!", status_code=status.HTTP_404_NOT_FOUND)
    else:
        if usuario in projeto.membros:
            raise HTTPException(detail="Este usuário já é membro desse Projeto!", status_code=status.HTTP_404_NOT_FOUND)
        else:
            projeto.membros.append(usuario)

            db.add(projeto)
            db.commit()
            return HTTPException(detail="Membro adicionado com sucesso com sucesso!", status_code=status.HTTP_201_CREATED)

    
#DELETE laboratorio
@router.delete('/removeMember/{projeto_id}/{member_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_member_project(projeto_id: str, member_id: str, db: Session = Depends(get_session), usuario_logado: Usuario = Depends(get_current_user)):
   
    query = select(Projeto).filter(Projeto.id == projeto_id).filter(projeto.autor_id == usuario_logado.id)
    result = db.execute(query)
    projeto: Projeto = result.scalars().unique().one_or_none()

    for member in projeto.membros:
        if member.id == member_id:
            db.delete(member)
            db.commit()
            return Response(detail="Membro removido com sucesso!", status_code=status.HTTP_204_NO_CONTENT)
    
    else:
        raise HTTPException(detail="Membro não encontrado!", status_code=status.HTTP_404_NOT_FOUND)
        
#DELETE laboratorio
@router.delete('/{projeto_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_projeto(projeto_id: str, db: Session = Depends(get_session), usuario_logado: Usuario = Depends(get_current_user)):
    query = select(Projeto).filter(Projeto.id == projeto_id).filter(Projeto.autor_id == usuario_logado.id)
    result = db.execute(query)
    laboratorio_del: Projeto = result.scalars().unique().one_or_none()

    if laboratorio_del:
        
        db.delete(laboratorio_del)
        db.commit()
        
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    
    else:
        raise HTTPException(detail="Laboratorio não encontrado!", status_code=status.HTTP_404_NOT_FOUND)