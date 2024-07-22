from typing import List

from fastapi import APIRouter, status, Depends, HTTPException, Response
from fastapi.security import  OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from sqlalchemy.future import select 
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from models.usuario import Usuario
from models.laboratorio import Laboratorio
from models.permissao import Permissao
from models.pending import Pending
from models.genero import Genero
from schemas.usuario_schema import UsuarioSchemaBase, UsuarioSchemaCreate, UsuarioSchemaUp, UsuarioSchemaLaboratoriosAndProjetos
from schemas.pending_schema import PendingSchema
from core.deps import get_current_user, get_session,process_image
from core.security import gerar_hash_senha
from core.auth import autenticar, criar_token_acesso
from sqlalchemy.orm import selectinload
from datetime import datetime


router = APIRouter()

# Autenticate
@router.get('/auth')
async def auth_user(usuario_logado: Usuario = Depends(get_current_user)):
    credential_exception: HTTPException = HTTPException(
        status_code= status.HTTP_200_OK,
        detail='Usuário autenticado com sucesso!',
        headers={"WWW-Authenticate": "Bearer"}
    )
    return credential_exception

# GET Logado
@router.get('/logado', response_model= UsuarioSchemaBase)
async def get_logado(usuario_logado: Usuario = Depends(get_current_user)):
    return usuario_logado

#POST Signup
@router.post('/signup', status_code=status.HTTP_201_CREATED, response_model=UsuarioSchemaBase)
async def post_usuario(usuario: UsuarioSchemaCreate, db: Session = Depends(get_session)):
    query = select(Genero).filter(Genero.id == usuario.genero)
    result = db.execute(query)
    genero: Genero = result.scalars().unique().one_or_none()

    if genero is None:
        raise HTTPException(detail="Genero não encontrado", status_code=status.HTTP_404_NOT_FOUND)

    # Verificar se a matrícula já existe
    matricula_existente = db.execute(select(Usuario).filter(Usuario.matricula == usuario.matricula)).first()
    if matricula_existente:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Matrícula já existe")
    
     # Processar a imagem se ela não for nula
    processed_image = None
    if usuario.image:
        processed_image = process_image(usuario.image)

    novo_usuario: Usuario = Usuario(
        senha=gerar_hash_senha(usuario.senha),
        primeiro_nome=usuario.primeiro_nome,
        primeiro_acesso=True,
        ativo=False,
        image=processed_image,
        segundo_nome=usuario.segundo_nome,
        data_nascimento=usuario.data_nascimento,
        email=usuario.email,
        genero=genero.id,
        matricula=usuario.matricula,
        tel=usuario.tel,
    )

    try:
        db.add(novo_usuario)
        db.commit()
        db.refresh(novo_usuario)

        return novo_usuario
    except IntegrityError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

# GET Usuarios
@router.get('/', response_model=List[UsuarioSchemaBase])
async def get_usuarios(db = Depends(get_session)):
    with db as session:
        query = select(Usuario)
        result = session.execute(query)
        usuarios: List[UsuarioSchemaBase] = result.scalars().unique().all() 

        return usuarios
    
@router.get('/{usuario_id}', response_model=UsuarioSchemaLaboratoriosAndProjetos, status_code=status.HTTP_200_OK)
async def get_usuario(usuario_id: str, db= Depends(get_session)):
    with db as session:
        query = select(Usuario).options(selectinload(Usuario.laboratorios), selectinload(Usuario.projetos)).filter(Usuario.id == usuario_id)
        result = session.execute(query)
        usuario = result.scalars().first()

        if usuario:
            return usuario
        else:
            raise HTTPException(detail='Usuário não encontrado.', status_code=status.HTTP_404_NOT_FOUND)
        
#PUT Usuario
@router.put('/{usuario_id}', response_model=UsuarioSchemaBase, status_code=status.HTTP_202_ACCEPTED)
async def put_usuario(usuario_id: str, usuario: UsuarioSchemaUp, db=Depends(get_session), usuario_logado: Usuario = Depends(get_current_user)):
    if usuario_logado:
        list_aux: List[Permissao] = []
        with db as session:
            query= select(Usuario).filter(Usuario.id == usuario_id)
            result= session.execute(query)
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
                if usuario.image:
                    usuario_up.image = process_image(usuario.image)
                if usuario.data_nascimento:
                    usuario_up.data_nascimento = usuario.data_nascimento
                if usuario.genero:
                    query = select(Genero).filter(Genero.id == usuario.genero)
                    result = db.execute(query)
                    genero: Genero = result.scalars().unique().one_or_none()
                    
                    if genero is None:
                        raise HTTPException(detail="Genero não encontrado", status_code=status.HTTP_404_NOT_FOUND)
                    else:
                        usuario_up.genero = genero.id
                if usuario.list_permissoes:
                    query= select(Permissao)
                    result= db.execute(query)
                    permissoes: List[Permissao] = result.scalars().unique().all()

                    for item in usuario.list_permissoes:
                        for permissao in permissoes:
                            if item == permissao.id:
                                list_aux.append(permissao)

                    usuario_up.permissoes.clear()
                    usuario_up.permissoes = list_aux
                if usuario.tel:
                    usuario_up.tel = usuario.tel

                usuario_up.data_atualizacao = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                session.commit()

                return usuario_up
            else:
                raise HTTPException(detail='Usuário não encontrado.', status_code=status.HTTP_404_NOT_FOUND)
        

@router.delete('/{usuario_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_usuario(usuario_id: str, db=Depends(get_session), usuario_logado: Usuario = Depends(get_current_user)):
    if usuario_logado:
        with db as session:
            # Verifica se o usuário é coordenador de algum laboratório
            query_coordenador = select(Laboratorio).filter(Laboratorio.coordenador_id == usuario_id)
            result_coordenador = session.execute(query_coordenador)
            laboratorios_coordenador: Laboratorio = result_coordenador.scalars().unique().one_or_none()

            if laboratorios_coordenador:
                raise HTTPException(
                    detail='Para você excluir sua conta, primeiro deve passar os direitos de coordenador para outro membro do laboratório!',
                    status_code=status.HTTP_400_BAD_REQUEST
                )

            # Se o usuário não for coordenador de nenhum laboratório, exclui o usuário
            query_usuario = select(Usuario).filter(Usuario.id == usuario_id)
            result_usuario = session.execute(query_usuario)
            usuario_del: Usuario = result_usuario.scalars().unique().one_or_none()

            if usuario_del:
                session.query(Pending).filter(Pending.id_user == usuario_del.id).delete()
                session.delete(usuario_del)
                session.commit()

                return Response(status_code=status.HTTP_204_NO_CONTENT)
            else:
                raise HTTPException(detail='Usuário não encontrado.', status_code=status.HTTP_404_NOT_FOUND)

#POST Login
@router.post('/login')
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db=Depends(get_session)):
    usuario = autenticar(email=form_data.username, senha=form_data.password, db=db)

    if not usuario:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Dados de acesso incorretos.')
    
    return JSONResponse(content={"access_token": criar_token_acesso(sub=usuario.id), "token_type":"bearer"}, status_code=status.HTTP_200_OK)


############################### Pedidos de acesso #############################

#POST Pedido de acesso ao laboratorio
@router.post('/requestAcessLab', status_code=status.HTTP_201_CREATED)
async def post_pending_laboratory(
    pending: PendingSchema, 
    usuario_logado: Usuario = Depends(get_current_user), 
    db: Session = Depends(get_session)
):
    query = select(Laboratorio).filter(Laboratorio.id == pending.id_lab)
    result = db.execute(query)
    laboratorio: Usuario = result.scalars().unique().one_or_none()

    if laboratorio is None:
        raise HTTPException(detail="Laboratório não encontrado!", status_code=status.HTTP_404_NOT_FOUND)
    
    for item in laboratorio.lista_acess:
        if item.id_user == pending.id_user:
            raise HTTPException(detail="Já existe um pedido seu nesse laboratório", status_code=status.HTTP_406_NOT_ACCEPTABLE)
        
    novo_pedido: Pending = Pending(
        id_user= pending.id_user,
        id_lab= pending.id_lab
    )

    laboratorio.lista_acess.append(novo_pedido)
    db.add(laboratorio)
    db.commit()