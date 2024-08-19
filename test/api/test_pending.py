def test_create_pending(db, client, token):
    db_session, user_id, genero_id, perm_id, lab_id, permLab, project_id, pedido_id, matricula, user2 = db
    object = {
      "id_user": str(user_id),
      "matricula_user": 2018030497
    }
    assert token is not None
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = client.post('/gestorlab/pendentes', headers=headers,json=object)
    assert response.status_code == 201

def test_get_pedidos(client):
    response = client.get('/gestorlab/pendentes')
    assert response.status_code == 200