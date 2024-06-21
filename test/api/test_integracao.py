from test.utils.utils_usuario import create_user_valido, update_user
from test.utils.utils_laboratorio import update_laboratorio, create_laboratorio
from test.utils.utils_project import update_projeto

## Teste Usuario
def test_post_usuario(client):
    body = create_user_valido()
    response = client.post('/gestorlab/usuarios/signup', json=body)
    assert response.status_code == 201

def test_login_usuario(client):
    login_data = {
        "username": "jfmaia.dev@gmail.com",
        "password": "p4ssw0rd"
    }
    response = client.post('/gestorlab/usuarios/login', data=login_data)
    assert response.status_code == 200
    token = response.json().get('access_token')
    
    return token

def test_usuario_logado(client):
    token = test_login_usuario(client)
    assert token is not None
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = client.get('/gestorlab/usuarios/logado', headers=headers)
    assert response.status_code == 200

def test_get_usuarios(client):
    response = client.get('/gestorlab/usuarios')
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_get_usuario(db,client):
    db_session, user_id, _, _= db
    response = client.get(f"/gestorlab/usuarios/{user_id}")
    assert response.status_code == 200

def test_update_usuario(db, client):
    db_session, user_id, _, _ = db
    token = test_login_usuario(client)
    assert token is not None
    headers = {
        "Authorization": f"Bearer {token}"
    }
    data ={
        "primeiro_nome": "José Flávio",
        "segundo_nome": "Maia",
        "email": "jfmaia.dev2@gmail.com",
        "matricula": 31234567891,
        "tel":84999314153,
        "tag":1,
        "senha":"password741@"
    }
    response = client.put(f"/gestorlab/usuarios/{user_id}", headers= headers, json=data)
    assert response.status_code == 202

def test_create_laboratorio(client):
    token = test_login_usuario(client)
    assert token is not None
    headers = {
        "Authorization": f"Bearer {token}"
    }
    data = create_laboratorio()
    response = client.post('/gestorlab/laboratorios/', headers=headers,json=data)
    assert response.status_code == 201

def test_delete_coordenado_of_laboratory(db, client):
    db_session, user_id, _, _ = db
    token = test_login_usuario(client)
    assert token is not None
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = client.delete(f"/gestorlab/usuarios/{user_id}", headers=headers)
    assert response.status_code == 400
    assert "Para você excluir sua conta, primeiro deve passar os direitos de coordenador para outro membro do laboratório!" in response.text

## Teste Laboratorios
def test_get_laboratorios(client):
    response = client.get('/gestorlab/laboratorios/')
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_get_laboratorio(db, client):
    db_session, _,lab_id, _ = db
    response = client.get(f"/gestorlab/laboratorios/{lab_id}")
    assert response.status_code == 200

def test_update_laboratorio(db, client):
    db_session, _, lab_id, _ = db
    token = test_login_usuario(client)
    assert token is not None
    headers = {
        "Authorization": f"Bearer {token}"
    }
    data = update_laboratorio()
    response = client.put(f"/gestorlab/laboratorios/{str(lab_id)}",headers=headers, json=data)
    assert response.status_code == 202

def test_add_member_lab(db, client):
    db_session, user_id, lab_id, _ = db
    object = {
        "idLaboratorio":str(lab_id),
        "idUser":str(user_id)
    }
    token = test_login_usuario(client)
    assert token is not None

    headers = {
        "Authorization": f"Bearer {token}"
    }
    # Certifique-se de que a URL está correta
    url = f"/gestorlab/laboratorios/addMember"
    response = client.post(url, headers=headers, json=object)
    assert response.status_code == 201

def test_delete_member_laboratorio(db, client):
    db_session, user_id, lab_id, _ = db
    token = test_login_usuario(client)
    assert token is not None
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = client.delete(f"/gestorlab/laboratorios/removeMember/{lab_id}/{user_id}",headers=headers)
    assert response.status_code == 204

def test_delete_laboratory(db, client):
    db_session, _, lab_id, _ = db
    token = test_login_usuario(client)
    assert token is not None
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = client.delete(f"/gestorlab/laboratorios/{lab_id}",headers=headers)
    assert response.status_code == 204

## Teste Projeto
def test_create_projeto(db, client):
    db_session, _, lab_id, _ = db
    object = {
        "titulo": "Criação de estufas tecnologicas nas escolas publicas de Caicó - CETPC",
        "descricao": "Projeto focado no ensinamentos tecnologicos no ambito da programação para auxiliar e ajudar jovens das escolas publicas de Caicó aprenderem como criar e da manutenção a uma estufa para legumes com automação tecnologica usando placas de Arduino para isso!",
        "labCreator": str(lab_id)
    }
    token = test_login_usuario(client)
    assert token is not None
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = client.post('/gestorlab/projetos/', headers=headers,json=object)
    assert response.status_code == 201

def test_get_projetos(client):
    response = client.get('/gestorlab/projetos')
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_get_projeto(db, client):
    db_session, _,_, project_id= db
    response = client.get(f"/gestorlab/projetos/{project_id}")
    assert response.status_code == 200

def test_update_projeto(db, client):
    db_session, _, _,  project_id = db
    token = test_login_usuario(client)
    assert token is not None
    headers = {
        "Authorization": f"Bearer {token}"
    }
    data =  update_projeto()
    response = client.put(f"/gestorlab/projetos/{project_id}",headers=headers, json=data)
    assert response.status_code == 202

def test_add_member_project(db, client):
    db_session, user_id, _, project_id = db
    object = {
        "idProjeto": str(project_id),
        "idUsuario": str(user_id)
    }
    token = test_login_usuario(client)
    assert token is not None

    headers = {
        "Authorization": f"Bearer {token}"
    }
    # Certifique-se de que a URL está correta
    url = f"/gestorlab/projetos/addMember"
    response = client.post(url, headers=headers, json= object)
    assert response.status_code == 201

def test_delete_member_projeto(db, client):
    db_session, user_id, _,  project_id = db
    token = test_login_usuario(client)
    assert token is not None
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = client.delete(f"/gestorlab/projetos/removeMember/{project_id}/{user_id}",headers=headers)
    assert response.status_code == 204

def test_delete_projeto(db, client):
    db_session, _, _,  project_id = db
    token = test_login_usuario(client)
    assert token is not None
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = client.delete(f"/gestorlab/projetos/{project_id}",headers=headers)
    assert response.status_code == 204

## Delete the user

def test_delete_user(db, client):
    db_session, user_id, _, _ = db
    token = test_login_usuario(client)
    assert token is not None
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = client.delete(f"/gestorlab/usuarios/{user_id}", headers=headers)
    assert response.status_code == 204
    
