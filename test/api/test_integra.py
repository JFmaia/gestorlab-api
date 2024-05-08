from test.utils.utils_usuario import create_user_valido

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
    primeiro_usuario = response.json()[0]
    id_usuario = primeiro_usuario.get('id')
    assert id_usuario is not None

    return id_usuario

def test_get_usuario(client):
    id_usuario = test_get_usuarios(client)
    response = client.get(f"/gestorlab/usuarios/{id_usuario}")
    assert response.status_code == 200
    id_usuario = response.json().get('id')

    return id_usuario

def test_update_usuario(client):
    data = {
        "primeiro_nome": "José Flávio da S.",
        "segundo_nome": "Maia",
        "email": "jfmaia.dev@gmail.com",
        "senha": "p4ssw0rd",
        "matricula": 12345678924,
        "tel": 84999314153,
        "tag": 2
    }
    id_usuario = test_get_usuario(client)
    response = client.put(f"/gestorlab/usuarios/{id_usuario}", json=data)
    assert response.status_code == 202

def test_create_laboratorio(client):
    id_usuario = test_get_usuarios(client)
    token = test_login_usuario(client)
    assert token is not None
    headers = {
        "Authorization": f"Bearer {token}"
    }
    data = {
        "nome": "Labens",
        "descricao": "Muito bom",
        "sobre": "gosto daqui",
        "template": 1,
        "email": "labens@gmail.com",
        "membros": [id_usuario],
    }
    response = client.post('/gestorlab/laboratorios/', headers=headers,json=data)
    print(response.json())
    assert response.status_code == 201


def test_delete_coordenado_of_laboratory(client):
    id_usuario = test_get_usuario(client)
    response = client.delete(f"/gestorlab/usuarios/{id_usuario}")
    assert response.status_code == 400
    assert "Para você excluir sua conta, primeiro deve passar os direitos de coordenador para outro membro do laboratório!" in response.text

def test_get_laboratorios(client):
    response = client.get('/gestorlab/laboratorios/')
    assert response.status_code == 200
    assert len(response.json()) > 0
    primeiro_laboratorio = response.json()[0]
    id_laboratorio = primeiro_laboratorio.get('id')
    assert id_laboratorio is not None

    return id_laboratorio

def test_get_laboratorio(client):
    id_laboratorio = test_get_laboratorios(client)
    response = client.get(f"/gestorlab/laboratorios/{id_laboratorio}")
    assert response.status_code == 200
    id_laboratorio = response.json().get('id')

    return id_laboratorio

def test_update_laboratorio(client):
    id_laboratorio = test_get_laboratorio(client)
    token = test_login_usuario(client)
    assert token is not None
    headers = {
        "Authorization": f"Bearer {token}"
    }
    data = {
        "nome": "Labens1",
        "descricao": "Um laboratorio focado para gerencia de dados e manippulação de banco de dados!",
        "sobre": "Laboratorio limpo, com pessoa legas e interessantes!",
        "template": 2,
        "email": "labens2@gmail.com",
    }
    response = client.put(f"/gestorlab/laboratorios/{id_laboratorio}",headers=headers, json=data)
    assert response.status_code == 202

def test_add_member_lab(client):
    id_laboratorio = test_get_laboratorio(client)
    member_email = "jfmaia.dev@gmail.com"
    token = test_login_usuario(client)
    assert token is not None
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = client.post(f"/gestorlab/laboratorios/addMember/{id_laboratorio}/{member_email}", headers=headers)
    # Adicione instruções de impressão para depuração
    print("Status Code da resposta:", response.status_code)
    print("Texto da resposta:", response.text)
    assert response.status_code == 201