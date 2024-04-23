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
        "email": "jfmaia741@gmail.com",
        "senha": "p4ssw0rd3",
        "matricula": 12345678924,
        "tel": 84999314153,
        "tag": 2
    }
    id_usuario = test_get_usuario(client)
    response = client.put(f"/gestorlab/usuarios/{id_usuario}", json=data)
    assert response.status_code == 202

def test_delete_usuario(client):
    id_usuario = test_get_usuario(client)
    response = client.delete(f"/gestorlab/usuarios/{id_usuario}")
    assert response.status_code == 204