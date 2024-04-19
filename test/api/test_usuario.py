# from test.utils.utils_usuario import create_user_valido

def test_get_usuarios(client):
    response = client.get('/gestorlab/usuarios')
    assert response.status_code == 200