from typing import List, Optional, Any

from fastapi import APIRouter, status, Depends, HTTPException, Response
from fastapi.security import  OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select 
from sqlalchemy.exc import IntegrityError

from models.usuario import Usuario
from schemas.usuario_schema import UsuarioSchemaBase, UsuarioSchemaCreate, UsuarioSchemaUp, UsuarioSchemaLaboratoriosAndProjetos
from core.deps import get_current_user, get_session
from core.security import gerar_hash_senha
from core.auth import autenticar, criar_token_acesso


router = APIRouter()


# GET Logado
@router.get('/logado', response_model= UsuarioSchemaBase)
def get_logado(usuario_logado: Usuario = Depends(get_current_user)):
    return usuario_logado

#POST / Signup
@router.post('/signup', status_code=status.HTTP_201_CREATED, response_model=UsuarioSchemaBase)
async def post_usuario(usuario: UsuarioSchemaCreate, db: AsyncSession = Depends(get_session)):
    novo_usuario: Usuario = Usuario(
        senha=gerar_hash_senha(usuario.senha),
        primeiro_nome=usuario.nome,
        segundo_nome=usuario.nome,
        email=usuario.email,
        matricula=usuario.matricula,
        tel=usuario.tel,
        data_inicial= usuario.data_inicial,
        data_atualizacao=usuario.data_atualizacao,
        tag=usuario.tag
    )

    async with db as session:
        try:
            session.add(novo_usuario)
            await session.commit()

            return novo_usuario
        except IntegrityError:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Já existe um usuario com essa matrícula cadastrada!")

# GET Usuarios
@router.get('/', response_model=List[UsuarioSchemaBase])
async def get_usuarios(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(Usuario)
        result = await session.execute(query)
        usuarios: List[UsuarioSchemaBase] = result.scalars().unique().all() 

        return usuarios
    
#Get usuario
@router.get('/{usuario_id}', response_model=UsuarioSchemaLaboratoriosAndProjetos, status_code=status.HTTP_200_OK)
async def get_usuario(usuario_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query= select(Usuario).filter(Usuario.id == usuario_id)
        result= await session.execute(query)
        usuario: UsuarioSchemaLaboratoriosAndProjetos = result.scalars().unique().one_or_none()

        if usuario:
            return usuario
        else:
            raise HTTPException(detail='Usuário não encontrado.', status_code=status.HTTP_404_NOT_FOUND)
        
#PUT Usuario
@router.put('/{usuario_id}', response_model=UsuarioSchemaBase, status_code=status.HTTP_202_ACCEPTED)
async def put_usuario(usuario_id: int, usuario: UsuarioSchemaUp, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query= select(Usuario).filter(Usuario.id == usuario_id)
        result= await session.execute(query)
        usuario_up: UsuarioSchemaBase = result.scalars().unique().one_or_none()

        if usuario_up:
            if usuario.primeiro_nome:
                usuario_up.primeiro_nome = usuario.primeiro_nome
            if usuario.segundo_nome:
                usuario_up.segundo_nome = usuario.segundo_nome
            if usuario.email:
                usuario_up.email = usuario.email
            if usuario.matricula:
                usuario_up.matricula = usuario.matricula
            if usuario.senha:
                usuario_up.senha = gerar_hash_senha(usuario.senha)
            if usuario.tag:
                usuario_up.tag = usuario.tag
            if usuario.data_inicial:
                usuario_up.data_inicial = usuario.data_inicial
            if usuario.data_atualizacao:
                usuario_up.data_atualizacao = usuario.data_atualizacao
            if usuario.tel:
                usuario_up.tel = usuario.tel

            await session.commit()

            return usuario_up
        else:
            raise HTTPException(detail='Usuário não encontrado.', status_code=status.HTTP_404_NOT_FOUND)
        
#DELETE Usuario
@router.delete('/{usuario_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_usuario(usuario_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query= select(Usuario).filter(Usuario.id == usuario_id)
        result= await session.execute(query)
        usuario_del: UsuarioSchemaBase = result.scalars().unique().one_or_none()

        if usuario_del:
            await session.delete(usuario_del)
            await session.commit()

            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail='Usuário não encontrado.', status_code=status.HTTP_404_NOT_FOUND)
        

#POST Login
@router.post('/login')
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_session)):
    usuario = await autenticar(email=form_data.username, senha=form_data.password, db=db)

    if not usuario:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Dados de acesso incorretos.')
    
    return JSONResponse(content={"access_token": criar_token_acesso(sub=usuario.id), "token_type":"bearer"}, status_code=status.HTTP_200_OK)