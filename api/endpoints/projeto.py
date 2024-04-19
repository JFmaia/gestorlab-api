from typing import List

from fastapi import APIRouter, status, Depends, HTTPException, Response

from sqlalchemy.future import  select

from models.projeto import Projeto
from models.usuario import Usuario
from schemas.projeto_schema import ProjetoSchema,ProjetoSchemaCreate,ProjetoSchemaUp
from core.deps import get_session, get_current_user
from datetime import datetime

router = APIRouter()

#POST Projeto
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=ProjetoSchema)
async def post_projeto(
    projeto: ProjetoSchemaCreate, 
    usuario_logado: Usuario = Depends(get_current_user), 
    db= Depends(get_session)
):
    with db as session:
        query = select(Usuario)
        result = session.execute(query)
        usuarios: List[Usuario] = result.scalars().unique().all()

    membrosList: List[Usuario] = []

    for id in projeto.membros:
        # Verificar se o membro está na lista de usuários
        for usuario in usuarios:
            if id == usuario.id:
                membrosList.append(usuario)
    
    novo_projeto: Projeto = Projeto(
        autor_id= usuario_logado.id,
        titulo = projeto.titulo,
        descricao= projeto.descricao,
        membros = membrosList
    )

    with db as session:
        query = select(Projeto).filter(Projeto.titulo == novo_projeto.titulo)
        result = session.execute(query)
        veryfProjeto: Projeto = result.scalars().unique().one_or_none()

    if(veryfProjeto):
        raise HTTPException(detail="Já existe um projeto com esse nome!!", status_code=status.HTTP_403_FORBIDDEN)
    else:
        db.add(novo_projeto)
        db.commit()
        return novo_projeto

    

#GET Projetos
@router.get('/', response_model= List[ProjetoSchema], status_code=status.HTTP_200_OK)
async def get_projetos(db= Depends(get_session)):
    with db as session:
        query = select(Projeto)
        result = session.execute(query)
        projetos: List[Projeto] = result.scalars().unique().all()

    return projetos

#GET Projeto
@router.get('/{projeto_id}', response_model= ProjetoSchema, status_code=status.HTTP_200_OK)
async def get_projeto(projeto_id: str, db= Depends(get_session)):
    with db as session:
        query = select(Projeto).filter(Projeto.id == projeto_id)
        result = session.execute(query)
        projeto: Projeto = result.scalars().unique().one_or_none()
    
    if projeto:
        return projeto
    else:
        raise HTTPException(detail="Projeto não encontrado", status_code=status.HTTP_404_NOT_FOUND)

#PUT Projeto
@router.put('/{projeto_id}', response_model=ProjetoSchema, status_code=status.HTTP_202_ACCEPTED)
async def put_projeto(projeto_id: str, projeto: ProjetoSchemaUp, db= Depends(get_session), usuario_logado: Usuario = Depends(get_current_user)):
    with db as session:
        query = select(Projeto).filter(Projeto.id == projeto_id)
        result = session.execute(query)
        projeto_up: Projeto = result.scalars().unique().one_or_none()
    
        if projeto_up:
            if projeto.titulo:
                projeto_up.titulo = projeto.titulo
            if projeto.membros:
                # Filtrar usuários pelo ID fornecido no corpo da solicitação
                membrosList = [usuario for usuario in projeto.membros]
                # Adicionar usuários à lista de membros se eles não estiverem lá
                for usuario_id in membrosList:
                    if usuario_id not in [membro.id for membro in projeto_up.membros]:
                        usuario = session.get(Usuario, usuario_id)
                        if usuario:
                            projeto_up.membros.append(usuario)
            else:
                # Se a lista de membros enviada estiver vazia, limpe a lista de membros do projeto
                projeto_up.membros = projeto.membros
           
            projeto_up.data_up = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            session.commit()
            return projeto_up
        
        else:
            raise HTTPException(detail="Projeto não encontrado!", status_code=status.HTTP_404_NOT_FOUND)
        
#DELETE Projeto
@router.delete('/{projeto_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_projeto(projeto_id: str, db= Depends(get_session), usuario_logado: Usuario = Depends(get_current_user)):
    with db as session:
        query = select(Projeto).filter(Projeto.id == projeto_id)
        result = session.execute(query)
        projeto_del: Projeto = result.scalars().unique().one_or_none()
    
        if projeto_del:
            if(projeto_del.autor_id == usuario_logado.id):
                session.delete(projeto_del)
                session.commit()
                return Response(status_code=status.HTTP_204_NO_CONTENT)
            else:
                raise HTTPException(detail="Você não tem permissão para excluir este projeto!", status_code=status.HTTP_403_FORBIDDEN)
        
        else:
            raise HTTPException(detail="Projeto não encontrado!", status_code=status.HTTP_404_NOT_FOUND)