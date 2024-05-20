from test.utils.utils_usuario import create_user_valido, update_user
from test.utils.utils_laboratorio import update_laboratorio, create_laboratorio

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
    db_session, user_id, _, _ = db
    response = client.get(f"/gestorlab/usuarios/{user_id}")
    assert response.status_code == 200

def test_update_usuario(db, client):
    data = update_user()
    db_session, user_id, _, _ = db
    response = client.put(f"/gestorlab/usuarios/{user_id}", json=data)
    assert response.status_code == 202

def test_create_laboratorio(client):
    token = test_login_usuario(client)
    assert token is not None
    headers = {
        "Authorization": f"Bearer {token}"
    }
    data = create_laboratorio()
    response = client.post('/gestorlab/laboratorios/', headers=headers,json=data)
    print(response.json())
    assert response.status_code == 201


def test_delete_coordenado_of_laboratory(db, client):
    db_session, user_id, _, _ = db
    response = client.delete(f"/gestorlab/usuarios/{user_id}")
    assert response.status_code == 400
    assert "Para você excluir sua conta, primeiro deve passar os direitos de coordenador para outro membro do laboratório!" in response.text

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
    response = client.put(f"/gestorlab/laboratorios/{lab_id}",headers=headers, json=data)
    assert response.status_code == 202

# def test_add_member_lab(db,client):
#     db_session, lab_id, _, _ = db
#     member_email = "admin@.com.br"
#     token = test_login_usuario(client)
#     assert token is not None
#     headers = {
#         "Authorization": f"Bearer {token}"
#     }
#     response = client.post(f"/gestorlab/laboratorios/addMember/{lab_id}/{member_email}", headers=headers)
#     # Adicione instruções de impressão para depuração
#     print("Status Code da resposta:", response.status_code)
#     print("Texto da resposta:", response.text)
#     assert response.status_code == 201