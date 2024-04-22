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

def test_usuario_logado(client):
    response = client.get('/gestorlab/usuarios/logado')
    assert response.status_code == 200

def test_get_usuarios(client):
    response = client.get('/gestorlab/usuarios')
    assert response.status_code == 200