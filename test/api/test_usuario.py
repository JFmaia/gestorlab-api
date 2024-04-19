from test.utils.utils_usuario import create_user_valido

def test_cria_usuario(client):
    body = create_user_valido()
    response = client.post('/gestorlab/usuarios/signup', json=body)
    assert response.status_code == 201