
def test_get_laboratorios(client):
    response = client.get('/gestorlab/laboratorios')
    assert response.status_code == 200

def test_get_laboratorio(db, client):
    db_session, user_id, genero_id, perm_id, lab_id, permLab, project_id, pedido_id, matricula, user2 = db
    response = client.get(f"/gestorlab/laboratorios/{lab_id}")
    assert response.status_code == 200

def test_update_laboratorio(db, client, token):
    db_session, user_id, genero_id, perm_id, lab_id, permLab, project_id, pedido_id, matricula, user2 = db
    assert token is not None
    headers = {
        "Authorization": f"Bearer {token}"
    }
    data = {
        "nome":"Labedoc",
        "sobre":"Laboratorio desenvolvimento de sistemas e banco de dados",
        "template": 1,
        "descricao":"Bom laboratorio de pesquisa de estudo tbm!!",
        "email":"labedoc@gmail.com",
        "endereco":{
            "logradouro": "Rua João Velho de Assis",
            "numero":123,
            "complemento":"Rua da farmacia velha",
            "bairro":"Monique",
            "cidade":"São Paulo",
            "estado":"RN",
            "cep":59300000,
            "pais":"Brasil"
        },
        "image":None
    }
    response = client.put(f"/gestorlab/laboratorios/{lab_id}",headers=headers, json=data)
    assert response.status_code == 202

def test_add_member_lab(db, client, token):
    db_session, user_id, genero_id, perm_id, lab_id, permLab, project_id, pedido_id, matricula, user2 = db
    object = {
        "idLaboratorio":str(lab_id),
        "idUser":str(user2),
        "perm_id": str(permLab)
    }
    assert token is not None

    headers = {
        "Authorization": f"Bearer {token}"
    }
   
    response = client.post("/gestorlab/laboratorios/addMember", headers=headers, json=object)
    assert response.status_code == 201

def test_invite_user(db, client, token):
    db_session, user_id, genero_id, perm_id, lab_id, permLab, project_id, pedido_id, matricula, user2 = db
   
    headers = {
        "Authorization": f"Bearer {token}"
    }
    data = {
        "id_lab":str(lab_id),
        "id_user":str(user_id)
    }
    response = client.post("/gestorlab/usuarios/requestAcessLab",headers=headers, json=data)

    assert response.status_code == 201


def test_delete_coordenado_of_laboratory(db, client, token):
    db_session, user_id, genero_id, perm_id, lab_id, permLab, project_id, pedido_id, matricula, user2 = db
    assert token is not None
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = client.delete(f"/gestorlab/usuarios/{user_id}", headers=headers)
    assert response.status_code == 400
    assert "Para você excluir sua conta, primeiro deve passar os direitos de coordenador para outro membro do laboratório!" in response.text

def test_update_permission_lab(db, client, token):
    db_session, user_id, genero_id, perm_id, lab_id, permLab, project_id, pedido_id, matricula, user2 = db
    assert token is not None
    headers = {
        "Authorization": f"Bearer {token}"
    }
    data = {
        "id":str(permLab),
        "id_lab": str(lab_id),
        "perm_id":str(perm_id)
    }
    response = client.post("/gestorlab/laboratorios/upPermission", headers=headers, json=data)    
    assert response.status_code == 202

def test_delete_laboratory(db, client, token):
    db_session, user_id, genero_id, perm_id, lab_id, permLab, project_id, pedido_id, matricula, user2 = db
    assert token is not None
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = client.delete(f"/gestorlab/laboratorios/{lab_id}",headers=headers)
    assert response.status_code == 204