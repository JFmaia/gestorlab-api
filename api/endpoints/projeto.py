import uuid
from typing import List
from datetime import datetime

from fastapi import APIRouter, status, Depends, HTTPException, Response

from sqlalchemy.future import  select
from sqlalchemy.ext.asyncio import AsyncSession

from models.projeto import Projeto
from models.usuario import Usuario
from models.associetions import usuario_projeto_association

from core.deps import get_session, get_current_user, process_image

from schemas.projeto_schema import ProjetoSchema, ProjetoSchemaCreate, ProjetoSchemaUp, ProjetoSchemaAddMember

router = APIRouter()

#POST Projeto
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=ProjetoSchema)
async def post_projeto(
    projeto: ProjetoSchemaCreate, 
    usuario_logado: Usuario = Depends(get_current_user), 
    db: AsyncSession = Depends(get_session)
):
    image_process= None
    if projeto.image:
        image_process= process_image(projeto.image)

    novo_projeto: Projeto = Projeto (
        autor_id= usuario_logado.id,
        titulo = projeto.titulo,
        descricao= projeto.descricao,
        lab_creator= projeto.labCreator,
        image= image_process
    )

    query = select(Projeto).filter(Projeto.titulo == novo_projeto.titulo)
    result = await db.execute(query)
    veryfProjeto: Projeto = result.scalars().unique().one_or_none()

    if(veryfProjeto):
        raise HTTPException(detail="Já existe um projeto com esse nome!!", status_code=status.HTTP_403_FORBIDDEN)
    else:
        db.add(novo_projeto)
        await db.commit()
        return novo_projeto

#GET Projetos
@router.get('/', response_model= List[ProjetoSchema], status_code=status.HTTP_200_OK)
async def get_projetos(db: AsyncSession = Depends(get_session)):
   
    query = select(Projeto)
    result = await db.execute(query)
    projetos: List[Projeto] = result.scalars().unique().all()

    return projetos

#GET Projeto
@router.get('/{projeto_id}', response_model= ProjetoSchema, status_code=status.HTTP_200_OK)
async def get_projeto(projeto_id: str, db: AsyncSession = Depends(get_session)):
   
    query = select(Projeto).filter(Projeto.id == projeto_id)
    result = await db.execute(query)
    projeto: Projeto = result.scalars().unique().one_or_none()
    
    if projeto:
        return projeto
    else:
        raise HTTPException(detail="Projeto não encontrado", status_code=status.HTTP_404_NOT_FOUND)

#PUT Projeto
@router.put('/{projeto_id}', response_model=ProjetoSchema, status_code=status.HTTP_202_ACCEPTED)
async def put_projeto(projeto_id: str, projeto: ProjetoSchemaUp, db: AsyncSession = Depends(get_session), usuario_logado: Usuario = Depends(get_current_user)):
    if usuario_logado:
        query = select(Projeto).filter(Projeto.id == projeto_id)
        result = await db.execute(query)
        projeto_up: Projeto = result.scalars().unique().one_or_none()

        if projeto_up:
            if projeto.titulo:
                projeto_up.titulo = projeto.titulo
            if projeto.descricao:
                projeto_up.descricao = projeto.descricao
                
            projeto_up.data_up = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            await db.commit()
            return projeto_up
        
        else:
            raise HTTPException(detail="Projeto não encontrado!", status_code=status.HTTP_404_NOT_FOUND)
        
##POST member in Project
@router.post('/addMember', status_code=status.HTTP_201_CREATED)
async def post_member(data: ProjetoSchemaAddMember, db: AsyncSession = Depends(get_session), usuario_logado: Usuario = Depends(get_current_user)): 
    if usuario_logado:
        query = select(Projeto).filter(Projeto.id == data.idProjeto)
        result = await db.execute(query)
        projeto:Projeto = result.scalars().unique().one_or_none()

        if projeto is None:
            raise HTTPException(detail="Projeto não encontrado!", status_code=status.HTTP_404_NOT_FOUND)

        query = select(Usuario).filter(Usuario.id == data.idUsuario)
        result = await db.execute(query)
        usuario: Usuario = result.scalars().unique().one_or_none()

        if usuario is None:
            raise HTTPException(detail="Usuario não encontrado!", status_code=status.HTTP_404_NOT_FOUND)
        else:
            if usuario in projeto.membros:
                raise HTTPException(detail="Este usuário já é membro desse Projeto!", status_code=status.HTTP_404_NOT_FOUND)
            else:
                projeto.membros.append(usuario)

                db.add(projeto)
                await db.commit()
                return HTTPException(detail="Membro adicionado com sucesso!", status_code=status.HTTP_201_CREATED)

    
#DELETE member projeto
@router.delete('/removeMember/{projeto_id}/{member_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_member_project(projeto_id: str, member_id: str, db: AsyncSession = Depends(get_session), usuario_logado: Usuario = Depends(get_current_user)):
    if usuario_logado:
        query = select(Projeto).filter(Projeto.id == projeto_id)
        result = await db.execute(query)
        projeto: Projeto = result.scalars().unique().one_or_none()

        if projeto is None:
            raise HTTPException(detail="Projeto não encontrado!", status_code=status.HTTP_404_NOT_FOUND)
        
        member_uuid = uuid.UUID(member_id)
        member_to_remove = None
        for member in projeto.membros:
            if member.id == member_uuid:
                member_to_remove = member
                break
            
        if member_to_remove:
            # Remover membro diretamente da tabela de associação
            delete_stmt = usuario_projeto_association.delete().where(
                usuario_projeto_association.c.projeto_id == projeto_id,
                usuario_projeto_association.c.usuario_id == member_id
            )
            db.execute(delete_stmt)
            await db.commit()
        else:
            raise HTTPException(detail="Membro não encontrado!", status_code=status.HTTP_404_NOT_FOUND)
        
#DELETE projeto
@router.delete('/{projeto_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_projeto(projeto_id: str, db: AsyncSession = Depends(get_session), usuario_logado: Usuario = Depends(get_current_user)):
    if usuario_logado:
        query = select(Projeto).filter(Projeto.id == projeto_id)
        result = await db.execute(query)
        projeto_del: Projeto = result.scalars().unique().one_or_none()

        if projeto_del:
            await db.delete(projeto_del)
            await db.commit()
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail="Projeto não encontrado!", status_code=status.HTTP_404_NOT_FOUND)
