from core.database import Session
from models.permissao import Permissao
from models.genero import Genero


def create_permissions():
    """Função para criar quatro permissões na tabela de permissão"""

    # Crie uma sessão do banco de dados
    session = Session()
    # Defina os nomes das permissões que deseja criar
    permissions = [
        "Admin",
        "Coordenador",
        "Membro"
    ]

    # Verifique se alguma permissão já existe antes de criar
    existing_permissions = session.query(Permissao).filter(Permissao.title.in_(permissions)).all()

    # Filtre as permissões que não existem ainda
    permissions_to_create = [perm for perm in permissions if perm not in [p.title for p in existing_permissions]]

    # Crie objetos Permissão para cada permissão que precisa ser criada
    new_permissions = [Permissao(title=perm) for perm in permissions_to_create]

    # Adicione as novas permissões à sessão
    session.add_all(new_permissions)

    # Confirme as alterações no banco de dados
    session.commit()

    # Feche a sessão
    session.close()

def create_generos():
    """Função para criar quatro permissões na tabela de permissão"""

    # Crie uma sessão do banco de dados
    session = Session()
    # Defina os nomes das permissões que deseja criar
    generos = [
        "Masculino", 
        "Feminino", 
        "Transgênero", 
        "Gênero neutro", 
        "Não-binário"
    ]

    # Verifique se alguma permissão já existe antes de criar
    existing_generos = session.query(Genero).filter(Genero.title.in_(generos)).all()

    # Filtre as permissões que não existem ainda
    genero_to_create = [gene for gene in generos if gene not in [p.title for p in existing_generos]]

    # Crie objetos Permissão para cada permissão que precisa ser criada
    new_genero = [Genero(title=gene) for gene in genero_to_create]

    # Adicione as novas permissões à sessão
    session.add_all(new_genero)

    # Confirme as alterações no banco de dados
    session.commit()

    # Feche a sessão
    session.close()

# Verifique se o script está sendo executado diretamente
if __name__ == "__main__":
    create_permissions()
    print("Permissões criadas com sucesso!")
    create_generos()
    print("Generos criados com sucesso!")