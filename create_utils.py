from core.database import Session
from models.permissao import Permissao
from models.permissaoLab import PermissaoOfLab
from models.genero import Genero
from core.security import gerar_hash_senha
from sqlalchemy.future import  select
from models.usuario import Usuario
from models.__all_models import *
from dotenv import load_dotenv
import os

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

EMAIL_USER: str = os.getenv('EMAIL_USER')
PASSWORD_USER: str = os.getenv('PASSWORD_USER')
   

def create_permissions():
    """Função para criar quatro permissões na tabela de permissão"""
    permissions = ["Admin", "Coordenador", "Membro"]
    
    with Session() as session:
        existing_permissions = session.query(Permissao).filter(Permissao.title.in_(permissions)).all()
        existing_titles = {p.title for p in existing_permissions}
        
        permissions_to_create = [perm for perm in permissions if perm not in existing_titles]
        new_permissions = [Permissao(title=perm) for perm in permissions_to_create]
        
        if new_permissions:
            session.add_all(new_permissions)
            session.commit()

def create_permissions_of_lab():
    """Função para criar quatro permissões na tabela de permissão"""
    permissions = ["Coolaborador", "Membro", "Supervisor"]
    
    with Session() as session:
        existing_permissions = session.query(PermissaoOfLab).filter(PermissaoOfLab.title.in_(permissions)).all()
        existing_titles = {p.title for p in existing_permissions}
        
        permissions_to_create = [perm for perm in permissions if perm not in existing_titles]
        new_permissions = [PermissaoOfLab(title=perm) for perm in permissions_to_create]
        
        if new_permissions:
            session.add_all(new_permissions)
            session.commit()

def create_generos():
    session = Session()
    generos = ["Masculino", "Feminino", "Transgênero", "Gênero neutro", "Não-binário"]
    existing_generos = session.query(Genero).filter(Genero.title.in_(generos)).all()
    genero_to_create = [gene for gene in generos if gene not in [p.title for p in existing_generos]]
    new_genero = [Genero(title=gene) for gene in genero_to_create]
    session.add_all(new_genero)
    session.commit()
    session.close()

def create_user_admin():
    session = Session()
    genero = session.query(Genero).first()

    query= select(Permissao).filter(Permissao.title == "Admin")
    result= session.execute(query)
    permission: Permissao = result.scalars().unique().one_or_none()

    if genero is None:
        print("Erro: Nenhum gênero encontrado.")
        return
    
    if permission is None:
        print("Erro: Nenhuma permissão encontrada.")
        return
    
    query= select(Usuario).filter(Usuario.email == EMAIL_USER)
    result= session.execute(query)
    usuario: Usuario = result.scalars().unique().one_or_none()
    if usuario:
        print("Usuário com matrícula já existe. Não foi criado um novo usuário.")
        session.close()
        return
    
    novo_usuario = Usuario(
        senha=gerar_hash_senha(PASSWORD_USER),
        primeiro_nome="Admin",
        primeiro_acesso=True,
        ativo=True,
        segundo_nome="Admin",
        data_nascimento="00/00/0000",
        email=EMAIL_USER,
        permissoes=[permission],
        genero=genero.id,
        matricula=0000000000,
        tel=00000000000,
    )
    session.add(novo_usuario)
    session.commit()
    session.close()

if __name__ == "__main__":
    create_permissions()
    print("Permissões criadas com sucesso!")
    create_permissions_of_lab()
    print("Permissões de laboratorio criadas com sucesso!")
    create_generos()
    print("Gêneros criados com sucesso!")
    create_user_admin()
    print("Admin criado com sucesso!")