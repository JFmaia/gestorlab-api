

def test_post_usuario(db,client):
  db_session, user_id, genero_id, perm_id, lab_id, permLab, project_id, pedido_id, matricula, user2 = db
  response = client.post(
    "/gestorlab/usuarios/signup",
      json={
        "primeiro_nome": "João",
        "segundo_nome": "Silva",
        "senha": "1234",
        "data_nascimento": "1990-01-01",
        "email": "joao.silva@example.com",
        "matricula": 123456789,
        "tel": 987654321,
        "id_genero": str(genero_id),  
        "image": None
      },
    )
  assert response.status_code == 201

def test_login_usuario(client):
    login_data = {
        "username": "admin@gmail.com",
        "password": "1234"
    }
    response = client.post('/gestorlab/usuarios/login', data=login_data)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert isinstance(data["access_token"], str)

def test_send_email(db, client, token):
    response = client.post(
        "/gestorlab/usuarios/sendEmail",
        json={
            "email":'admin@gmail.com'
        },
    )
  
    assert response.status_code == 202

def test_recovery_password(db, client, token):
    db_session, user_id, genero_id, perm_id, lab_id, permLab, project_id, pedido_id, matricula, user2 = db
    response = client.post(
        "/gestorlab/usuarios/passwordRecovery",
        json={
            "id_user": str(user_id),
            "senha": "1234"
        },
    )
    assert response.status_code == 200
    

def test_usuario_logado(client, token):
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
    db_session, user_id, genero_id, perm_id, lab_id, permLab, project_id, pedido_id, matricula, user2 = db
    response = client.get(f"/gestorlab/usuarios/{user_id}")
    assert response.status_code == 200

def test_update_usuario(db, client, token):
    db_session, user_id, genero_id, perm_id, lab_id, permLab, project_id, pedido_id, matricula, user2 = db
    assert token is not None
    headers = {
        "Authorization": f"Bearer {token}"
    }
    data = {
        "primeiro_nome": "José Flávio",
        "segundo_nome": "Maia",
        "id_perm": str(perm_id),
        "id_genero": str(genero_id),
        "data_nascimento":"08/08/2000",
        "email": "admin@gmail.com",
        "matricula": 31234567891,
        "tel": 84999314153,
        "image": None,
        "senha": "password741@"
    }
    response = client.put(f"/gestorlab/usuarios/{user_id}", headers=headers, json=data)    
    assert response.status_code == 202

def test_delete_user(db, client, token):
    db_session, user_id, genero_id, perm_id, lab_id, permLab, project_id, pedido_id, matricula, user2 = db
    assert token is not None
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = client.delete(f"/gestorlab/usuarios/{user2}", headers=headers)
    assert response.status_code == 204