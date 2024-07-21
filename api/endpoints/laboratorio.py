from typing import List
from uuid import UUID

from fastapi import APIRouter, status, Depends, HTTPException, Response

from sqlalchemy.future import  select
from sqlalchemy.orm import Session
from models.associetions import usuario_laboratorio_association
from models.laboratorio import Laboratorio
from models.usuario import Usuario
from models.permissao import Permissao
from models.permissao_lab import PermissaoLaboratorio
from schemas.laboratorio_schema import LaboratorioSchema, LaboratorioSchemaCreate, LaboratorioSchemaUp,  LaboratorioSchemaAddMember, PermissaoLaboratorioCreate, PermissaoLaboratorioResponse, PermissaoLaboratorioUp
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
async def get_laboratorios(db: Session = Depends(get_session)):
    query = select(Laboratorio)
    result = db.execute(query)
    laboratorios: List[Laboratorio] = result.scalars().unique().all()

    return laboratorios

#GET laboratorio
@router.get('/{laboratorio_id}', response_model= LaboratorioSchema, status_code=status.HTTP_200_OK)
async def get_laboratorio(laboratorio_id: str, db: Session = Depends(get_session)):
    query = select(Laboratorio).filter(Laboratorio.id == laboratorio_id)
    result = db.execute(query)
    laboratorio: Laboratorio = result.scalars().unique().one_or_none()
    
    if laboratorio:
        return laboratorio
    else:
        raise HTTPException(detail="laboratorio não encontrado", status_code=status.HTTP_404_NOT_FOUND)

#PUT laboratorio
@router.put('/{laboratorio_id}', response_model=LaboratorioSchema, status_code=status.HTTP_202_ACCEPTED)
async def put_laboratorio(laboratorio_id: str, laboratorio: LaboratorioSchemaUp, db: Session = Depends(get_session), usuario_logado: Usuario = Depends(get_current_user)):
    if usuario_logado:
        query = select(Laboratorio).filter(Laboratorio.id == laboratorio_id)
        result = db.execute(query)
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
            
            db.add(laboratorio_up)
            db.commit()
            
            return laboratorio_up
        
        else:
            raise HTTPException(detail="laboratorio não encontrado!", status_code=status.HTTP_404_NOT_FOUND)

## Upgrade permission laboratorio
@router.post('/upPermission', response_model=LaboratorioSchema, status_code=status.HTTP_202_ACCEPTED)
def update_perm(
    value: PermissaoLaboratorioUp,
    db: Session = Depends(get_session)
):
    # Verifica se a permissão existe
    db_permissao = db.query(Permissao).filter(Permissao.id == value.perm_id).first()
    if db_permissao is None:
        raise HTTPException(status_code=404, detail="Permissao not found")

    # Verifica se o laboratório existe
    query = select(Laboratorio).filter(Laboratorio.id == value.id_lab)
    result = db.execute(query)
    laboratorio_up: Laboratorio = result.scalars().unique().one_or_none()
    if laboratorio_up is None:
        raise HTTPException(status_code=404, detail="Laboratorio not found")
    
    # Verifica se já existe uma permissão de laboratório para o usuário e laboratório
    for perm in laboratorio_up.lista_perm:
        if perm.id == value.id:
            perm.perm_id = value.perm_id
    
    db.add(laboratorio_up)
    db.commit()
    return laboratorio_up
        
#POST member in laboratory
@router.post('/addMember', status_code=status.HTTP_201_CREATED)
async def post_member(user: LaboratorioSchemaAddMember , db: Session = Depends(get_session), usuario_logado: Usuario = Depends(get_current_user)):
    # Primeiro, obtenha o laboratório na mesma sessão
    if usuario_logado: 
        query = select(Laboratorio).filter(Laboratorio.id == user.idLaboratorio)
        result = db.execute(query)
        laboratorio: Laboratorio = result.scalars().unique().one_or_none()

        if laboratorio is None:
            raise HTTPException(detail="Laboratorio não encontrado!", status_code=status.HTTP_404_NOT_FOUND)

        # Em seguida, obtenha o usuário na mesma sessão
        query = select(Usuario).filter(Usuario.id == user.idUser)
        result = db.execute(query)
        usuario: Usuario = result.scalars().unique().one_or_none()

        if usuario is None:
            raise HTTPException(detail="Usuario não encontrado!", status_code=status.HTTP_404_NOT_FOUND)
        else:
            if usuario in laboratorio.membros:
                raise HTTPException(detail="Este usuário já é membro desse laboratorio!", status_code=status.HTTP_400_BAD_REQUEST)
            else:
                laboratorio.membros.append(usuario)

                db.add(laboratorio)
                db.commit()
                return {"detail": "Membro adicionado com sucesso com sucesso!"}



@router.delete('/removeMember/{laboratorio_id}/{member_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_member_laboratory(
    laboratorio_id: str, 
    member_id: str, 
    db: Session = Depends(get_session), 
    usuario_logado: Usuario = Depends(get_current_user)
):
    if usuario_logado:
        query = select(Laboratorio).filter(Laboratorio.id == laboratorio_id)
        result = db.execute(query)
        laboratorio: Laboratorio = result.scalars().unique().one_or_none()

        if laboratorio is None:
            raise HTTPException(detail="Laboratório não encontrado!", status_code=status.HTTP_404_NOT_FOUND)
        
        member_uuid = uuid.UUID(member_id)
        member_to_remove = None
        for member in laboratorio.membros:
            if member.id == member_uuid:
                member_to_remove = member
                break
        
        if member_to_remove:
            # Remover membro diretamente da tabela de associação
            delete_stmt = usuario_laboratorio_association.delete().where(
                usuario_laboratorio_association.c.laboratorio_id == laboratorio_id,
                usuario_laboratorio_association.c.usuario_id == member_uuid
            )
            db.execute(delete_stmt)
            db.commit()
        else:
            raise HTTPException(detail="Membro não encontrado!", status_code=status.HTTP_404_NOT_FOUND)
        

#DELETE laboratorio
@router.delete('/{laboratorio_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_laboratorio(laboratorio_id: str, db: Session = Depends(get_session), usuario_logado: Usuario = Depends(get_current_user)):
    if usuario_logado:
        query = select(Laboratorio).filter(Laboratorio.id == laboratorio_id)
        result = db.execute(query)
        laboratorio_del: Laboratorio = result.scalars().unique().one_or_none()

        if laboratorio_del:
            
            db.delete(laboratorio_del)
            db.commit()
            
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        
        else:
            raise HTTPException(detail="Laboratorio não encontrado!", status_code=status.HTTP_404_NOT_FOUND)
        

@router.post("/addPerm", response_model=PermissaoLaboratorioResponse)
def create_permissao_laboratorio(
    permissao_laboratorio: PermissaoLaboratorioCreate,
    db: Session = Depends(get_session)
):
    # Verifica se a permissão existe
    db_permissao = db.query(Permissao).filter(Permissao.id == permissao_laboratorio.perm_id).first()
    if db_permissao is None:
        raise HTTPException(status_code=404, detail="Permissao not found")

    # Verifica se o laboratório existe
    db_laboratorio = db.query(Laboratorio).filter(Laboratorio.id == permissao_laboratorio.id_lab).first()
    if db_laboratorio is None:
        raise HTTPException(status_code=404, detail="Laboratorio not found")
    
    # Verifica se já existe uma permissão de laboratório para o usuário e laboratório
    for perm in db_laboratorio.lista_perm:
        if perm.id_user == permissao_laboratorio.id_user:
            raise HTTPException(status_code=400, detail="Esse usuário já tem permissão no laboratório!")
    
    # Cria a nova permissão de laboratório
    db_permissao_laboratorio = PermissaoLaboratorio(
        id_user=permissao_laboratorio.id_user,
        id_lab=permissao_laboratorio.id_lab,
        perm_id=permissao_laboratorio.perm_id
    )
    db_laboratorio.lista_perm.append(db_permissao_laboratorio)
    db.add(db_laboratorio)
    db.commit()
    return db_permissao_laboratorio