def test_create_projeto(db, client, token):
    db_session, user_id, genero_id, perm_id, lab_id, permLab, project_id, pedido_id, matricula, user2 = db
    object = {
        "titulo": "Criação de estufas tecnologicas nas escolas publicas de Caicó - CETPC",
        "descricao": "Projeto focado no ensinamentos tecnologicos no ambito da programação para auxiliar e ajudar jovens das escolas publicas de Caicó aprenderem como criar e da manutenção a uma estufa para legumes com automação tecnologica usando placas de Arduino para isso!",
        "laboratorio_id": str(lab_id),
        "image": None
    }
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
    db_session, user_id, genero_id, perm_id, lab_id, permLab, project_id, pedido_id, matricula, user2 = db
    response = client.get(f"/gestorlab/projetos/{project_id}")
    assert response.status_code == 200

def test_update_projeto(db, client, token):
    db_session, user_id, genero_id, perm_id, lab_id, permLab, project_id, pedido_id, matricula, user2 = db
    assert token is not None
    headers = {
        "Authorization": f"Bearer {token}"
    }
    data =  {}
    response = client.put(f"/gestorlab/projetos/{project_id}",headers=headers, json=data)
    assert response.status_code == 202

def test_add_member_project(db, client, token):
    db_session, user_id, genero_id, perm_id, lab_id, permLab, project_id, pedido_id, matricula, user2 = db
    object = {
        "idProjeto": str(project_id),
        "idUsuario": str(user2)
    }
    assert token is not None

    headers = {
        "Authorization": f"Bearer {token}"
    }
    # Certifique-se de que a URL está correta
    url = f"/gestorlab/projetos/addMember"
    response = client.post(url, headers=headers, json= object)
    assert response.status_code == 201

def test_delete_projeto(db, client, token):
    db_session, user_id, genero_id, perm_id, lab_id, permLab, project_id, pedido_id, matricula, user2 = db
    assert token is not None
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = client.delete(f"/gestorlab/projetos/{project_id}",headers=headers)
    assert response.status_code == 204