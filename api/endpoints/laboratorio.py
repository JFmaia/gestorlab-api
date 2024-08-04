import uuid
from typing import List
from fastapi import APIRouter, status, Depends, HTTPException, Response
from datetime import datetime

from sqlalchemy.future import  select
from sqlalchemy.ext.asyncio import AsyncSession

from models.associetions import usuario_laboratorio_association
from models.laboratorio import Laboratorio
from models.usuario import Usuario
from models.permissao import Permissao
from models.permissaoLab import PermissaoOfLab
from models.pending import Pending
from models.permissao_lab import PermissaoLaboratorio

from core.deps import get_session, get_current_user, process_image

from schemas.pending_schema import PendingSchema
from schemas.laboratorio_schema import LaboratorioSchema, LaboratorioSchemaCreate, LaboratorioSchemaUp,  LaboratorioSchemaAddMember, PermissaoLaboratorioCreate, PermissaoLaboratorioResponse, PermissaoLaboratorioUp


router = APIRouter()


############################ End Points basicos do laboratorio  #############################

#POST Laboratorio
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=LaboratorioSchema)
async def post_laboratorio(
    laboratorio: LaboratorioSchemaCreate, 
    usuario_logado: Usuario = Depends(get_current_user), 
    db: AsyncSession = Depends(get_session)
):
    query = select(Usuario).filter(Usuario.id == usuario_logado.id)
    result = await db.execute(query)
    usuario_coord: Usuario= result.scalars().unique().one_or_none()

    queryPerm = select(PermissaoOfLab).filter(PermissaoOfLab.title == 'Coordenador')
    result = await db.execute(queryPerm)
    permition_coord: PermissaoOfLab = result.scalars().unique().one_or_none()

    processed_image = None
    if laboratorio.image:
        processed_image = process_image(laboratorio.image)

    novo_laboratorio: Laboratorio = Laboratorio(
        coordenador_id= usuario_logado.id,
        nome = laboratorio.nome,
        sobre= laboratorio.sobre,
        template= laboratorio.template,
        descricao= laboratorio.descricao,
        email= laboratorio.email,
        image= processed_image
    )

    novo_laboratorio.membros.append(usuario_coord)

    await db.add(novo_laboratorio)
    await db.commit()

    queryLab = select(Laboratorio).filter(Laboratorio.coordenador_id == usuario_logado.id)
    result = await db.execute(queryLab)
    laboratorio: Laboratorio = result.scalars().unique().one_or_none()

    permissao_laboratorio = PermissaoLaboratorio(
        id_user= usuario_logado.id,
        id_lab= laboratorio.id,
        perm_id= permition_coord.id 
    )

    laboratorio.lista_perm.append(permissao_laboratorio)
    await db.add(laboratorio)
    await db.commit() 

    return laboratorio

#GET Laboratorios
@router.get('/', response_model= List[LaboratorioSchema], status_code=status.HTTP_200_OK)
async def get_laboratorios(db:AsyncSession = Depends(get_session)):
    query = select(Laboratorio)
    result = await db.execute(query)
    laboratorios: List[Laboratorio] = result.scalars().unique().all()

    return laboratorios

#GET laboratorio
@router.get('/{laboratorio_id}', response_model= LaboratorioSchema, status_code=status.HTTP_200_OK)
async def get_laboratorio(laboratorio_id: str, db:AsyncSession = Depends(get_session)):
    query = select(Laboratorio).filter(Laboratorio.id == laboratorio_id)
    result = await db.execute(query)
    laboratorio: Laboratorio = result.scalars().unique().one_or_none()
    
    if laboratorio:
        return laboratorio
    else:
        raise HTTPException(detail="laboratorio não encontrado", status_code=status.HTTP_404_NOT_FOUND)

#PUT laboratorio
@router.put('/{laboratorio_id}', response_model=LaboratorioSchema, status_code=status.HTTP_202_ACCEPTED)
async def put_laboratorio(laboratorio_id: str, laboratorio: LaboratorioSchemaUp, db:AsyncSession = Depends(get_session), usuario_logado: Usuario = Depends(get_current_user)):
    if usuario_logado:
        query = select(Laboratorio).filter(Laboratorio.id == laboratorio_id)
        result = await db.execute(query)
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
            if laboratorio.image:
                laboratorio_up.image = process_image(laboratorio.image)
            
            laboratorio_up.data_up = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            await db.commit()
            
            return laboratorio_up
        
        else:
            raise HTTPException(detail="laboratorio não encontrado!", status_code=status.HTTP_404_NOT_FOUND)
        
#DELETE laboratorio
@router.delete('/{laboratorio_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_laboratorio(laboratorio_id: str, db:AsyncSession = Depends(get_session), usuario_logado: Usuario = Depends(get_current_user)):
    if usuario_logado:
        query = select(Laboratorio).filter(Laboratorio.id == laboratorio_id)
        result = await db.execute(query)
        laboratorio_del: Laboratorio = result.scalars().unique().one_or_none()

        if laboratorio_del:
            
            await db.delete(laboratorio_del)
            await db.commit()
            
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        
        else:
            raise HTTPException(detail="Laboratorio não encontrado!", status_code=status.HTTP_404_NOT_FOUND)
        

############################### End Points de membros do laboratorio #############################

#POST member in laboratory
@router.post('/addMember', status_code=status.HTTP_201_CREATED)
async def post_member(user: LaboratorioSchemaAddMember , db:AsyncSession = Depends(get_session), usuario_logado: Usuario = Depends(get_current_user)):
    # Primeiro, obtenha o laboratório na mesma sessão
    if usuario_logado: 
        query = select(Laboratorio).filter(Laboratorio.id == user.idLaboratorio)
        result = await db.execute(query)
        laboratorio: Laboratorio = result.scalars().unique().one_or_none()

        if laboratorio is None:
            raise HTTPException(detail="Laboratorio não encontrado!", status_code=status.HTTP_404_NOT_FOUND)

        # Em seguida, obtenha o usuário na mesma sessão
        query = select(Usuario).filter(Usuario.id == user.idUser)
        result = await db.execute(query)
        usuario: Usuario = result.scalars().unique().one_or_none()

        if usuario is None:
            raise HTTPException(detail="Usuario não encontrado!", status_code=status.HTTP_404_NOT_FOUND)
        else:
            if usuario in laboratorio.membros:
                raise HTTPException(detail="Este usuário já é membro desse laboratorio!", status_code=status.HTTP_400_BAD_REQUEST)
            else:
                laboratorio.membros.append(usuario)

                await db.add(laboratorio)
                await db.commit()
                return {"detail": "Membro adicionado com sucesso com sucesso!"}



@router.delete('/removeMember/{laboratorio_id}/{member_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_member_laboratory(
    laboratorio_id: str, 
    member_id: str, 
    db:AsyncSession = Depends(get_session), 
    usuario_logado: Usuario = Depends(get_current_user)
):
    if usuario_logado:
        query = select(Laboratorio).filter(Laboratorio.id == laboratorio_id)
        result = await db.execute(query)
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
            await db.execute(delete_stmt)
            await db.commit()
        else:
            raise HTTPException(detail="Membro não encontrado!", status_code=status.HTTP_404_NOT_FOUND)
        

############################### End Points de permissão do laboratorio #############################

@router.post("/addPerm", response_model=PermissaoLaboratorioResponse)
async def create_permissao_laboratorio(
    permissao_laboratorio: PermissaoLaboratorioCreate,
    db:AsyncSession = Depends(get_session)
):
    # Verifica se a permissão existe
    db_permissao = await db.query(PermissaoOfLab).filter(PermissaoOfLab.id == permissao_laboratorio.perm_id).first()
    if db_permissao is None:
        raise HTTPException(status_code=404, detail="Permissão encontrada")

    # Verifica se o laboratório existe
    db_laboratorio = await db.query(Laboratorio).filter(Laboratorio.id == permissao_laboratorio.id_lab).first()
    if db_laboratorio is None:
        raise HTTPException(status_code=404, detail="Laboratorio não encontrado")
    
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
    await db.add(db_laboratorio)
    await db.commit() 
    return db_permissao_laboratorio


## Upgrade permission laboratorio
@router.post('/upPermission', response_model=LaboratorioSchema, status_code=status.HTTP_202_ACCEPTED)
async def update_perm(
    value: PermissaoLaboratorioUp,
    db:AsyncSession = Depends(get_session)
):
    # Verifica se a permissão existe
    db_permissao = await db.query(Permissao).filter(Permissao.id == value.perm_id).first()
    if db_permissao is None:
        raise HTTPException(status_code=404, detail="Permissao not found")

    # Verifica se o laboratório existe
    query = select(Laboratorio).filter(Laboratorio.id == value.id_lab)
    result = await db.execute(query)
    laboratorio_up: Laboratorio = result.scalars().unique().one_or_none()
    if laboratorio_up is None:
        raise HTTPException(status_code=404, detail="Laboratorio not found")
    
    # Verifica se já existe uma permissão de laboratório para o usuário e laboratório
    for perm in laboratorio_up.lista_perm:
        if perm.id == value.id:
            perm.perm_id = value.perm_id
    
    await db.add(laboratorio_up)
    await db.commit()
    return laboratorio_up

############################### Pedidos de acesso #############################

#POST Pedido de acesso ao laboratorio
@router.post('/invitationUser', status_code=status.HTTP_201_CREATED)
async def post_invitation(
    pending: PendingSchema, 
    usuario_logado: Usuario = Depends(get_current_user), 
    db:AsyncSession = Depends(get_session)
):
    query = select(Usuario).filter(Usuario.id == pending.id_user)
    result = await db.execute(query)
    usuario: Usuario = result.scalars().unique().one_or_none()

    if usuario is None:
        raise HTTPException(detail="Usuário não encontrado!", status_code=status.HTTP_404_NOT_FOUND)
    
    for item in usuario.lista_pending:
        if item.id_lab == pending.id_lab:
            raise HTTPException(detail="Você já convidou este usuário!", status_code=status.HTTP_406_NOT_ACCEPTABLE)
        
    novo_pedido: Pending = Pending(
        id_user= pending.id_user,
        id_lab= pending.id_lab
    )

    usuario.lista_pending.append(novo_pedido)
    await db.add(usuario)
    await db.commit()