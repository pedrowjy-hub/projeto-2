import pytest
from unittest.mock import patch, MagicMock
from api import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


@patch("api.conectar_banco")
def test_lista_imoveis_vazios(mock_conectar_banco, client):

    mock_con = MagicMock()
    mock_cur = MagicMock()

    mock_con.cursor.return_value = mock_cur
    mock_cur.fetchall.return_value = []
    mock_conectar_banco.return_value = mock_con

    response = client.get("/imoveis")

    assert response.status_code == 200
    assert response.get_json() == []
    mock_cur.execute.assert_called_once_with(
        "SELECT id, logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao FROM imoveis"
    )
    mock_cur.fetchall.assert_called_once()
    mock_cur.close.assert_called_once()
    mock_con.close.assert_called_once()



@patch("api.conectar_banco")
def test_listar_imoveis_com_dados(mock_conectar_banco, client):

    mock_con = MagicMock()
    mock_cur = MagicMock()

    mock_con.cursor.return_value = mock_cur
    mock_cur.fetchall.return_value = [
        (1, "Panamby", "Avenida", "Morumbi", "Sao Paulo", "01000", "apartamento", 100000, "2026-09-08")
    ]
    mock_conectar_banco.return_value = mock_con

    response = client.get("/imoveis")

    assert response.status_code == 200
    assert response.get_json() == [
        {
            "id": 1,
            "logradouro": "Panamby",
            "tipo_logradouro": "Avenida",
            "bairro": "Morumbi",
            "cidade": "Sao Paulo",
            "cep": "01000",
            "tipo": "apartamento",
            "valor": 100000,
            "data_aquisicao": "2026-09-08"
        }
    ]
    mock_cur.execute.assert_called_once_with(
        "SELECT id, logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao FROM imoveis"
    )
    mock_cur.fetchall.assert_called_once()
    mock_cur.close.assert_called_once()
    mock_con.close.assert_called_once()

@patch('api.conectar_banco')
def test_lista_imoveis_especifico_ok(mock_conectar_banco,client):

    mock_con = MagicMock()
    mock_cur = MagicMock()

    mock_con.cursor.return_value = mock_cur

    mock_cur.fetchone.return_value = (1,'Panamby','Avenida','Morumbi','Sao Paulo','01000','apartamento',100000,'2026-09-08')
    mock_conectar_banco.return_value = mock_con

    response = client.get('/imoveis/1')

    assert response.status_code == 200
    assert response.get_json() == {
                "id": 1,
                "logradouro": "Panamby",
                "tipo_logradouro": "Avenida",
                "bairro": "Morumbi",
                "cidade": "Sao Paulo",
                "cep": "01000",
                "tipo": "apartamento",
                "valor": 100000,
                "data_aquisicao": "2026-09-08"
            }

    mock_cur.execute.assert_called_once_with('SELECT id, logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao FROM imoveis WHERE id = %s',
                                             (1,))

    mock_cur.fetchone.assert_called_once()
    mock_cur.close.assert_called_once()
    mock_con.close.assert_called_once()


@patch("api.conectar_banco")
def test_listar_imoveis_id_nao_existe(mock_conectar_banco, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchone.return_value = None
    mock_conectar_banco.return_value = mock_conn

    response = client.get("/imoveis/2000")

    assert response.status_code == 404
    assert response.get_json() == {"erro": "Imoveis não encontrado"}

    mock_cursor.execute.assert_called_once_with(
        "SELECT id, logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao FROM imoveis WHERE id = %s",
        (2000,),
    )
    mock_cursor.fetchone.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()

@patch("api.conectar_banco")
def test_adicionar_imovel(mock_conectar_banco, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.lastrowid = 2000

    mock_conectar_banco.return_value = mock_conn

    payload = {
                "logradouro": "Panamby",
                "tipo_logradouro": "Avenida",
                "bairro": "Morumbi",
                "cidade": "Sao Paulo",
                "cep": "01000",
                "tipo": "apartamento",
                "valor": 100000,
                "data_aquisicao": "2026-09-08"
            }
    response = client.post("/imoveis", json=payload)

    assert response.status_code == 201
    assert response.get_json() == {"id": 2000}

    mock_cursor.execute.assert_called_once_with(
        "INSERT INTO imoveis (logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
        ("Panamby", "Avenida", "Morumbi", "Sao Paulo", "01000", "apartamento", 100000, "2026-09-08"),
    )
    mock_conn.commit.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()

@patch('api.conectar_banco')
def test_adiciona_imovel_erro(mock_conectar_banco,client):
    response = client.post('/imoveis',json={'logradouro': 'Panamby'})

    assert response.status_code == 400
    assert response.get_json() == {"erro": "Campos obrigatórios: logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao"}

    mock_conectar_banco.assert_not_called()

@patch('api.conectar_banco')
def test_atualiza_imovel_ok(mock_conectar_banco,client):

    mock_con = MagicMock()
    mock_cur = MagicMock()

    mock_con.cursor.return_value = mock_cur

    mock_conectar_banco.return_value = mock_con

    payload = {     
                    "logradouro": "Panamby",
                    "tipo_logradouro": "Avenida",
                    "bairro": "Morumbi",
                    "cidade": "Sao Paulo",
                    "cep": "01000",
                    "tipo": "apartamento",
                    "valor": 100000,
                    "data_aquisicao": "2026-09-08"}

    response = client.put('/imoveis/1', json = payload)

    assert response.status_code == 200
    assert response.get_json() == {"mensagem": "Imovel atualizado com sucesso"}

    mock_cur.execute.assert_called_once_with('UPDATE imoveis SET logradouro = %s, tipo_logradouro = %s, bairro = %s, cidade = %s, cep = %s, tipo = %s, valor = %s, data_aquisicao = %s WHERE id = %s',
                                             ('Panamby','Avenida','Morumbi','Sao Paulo','01000','apartamento',100000,'2026-09-08',1))

    mock_con.commit.assert_called_once()
    mock_cur.close.assert_called_once()
    mock_con.close.assert_called_once()

@patch("api.conectar_banco")
def test_atualizar_contato_not_found(mock_conectar_banco, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.rowcount = 0
    mock_conectar_banco.return_value = mock_conn

    payload = {
                "logradouro": "Panamby",
                "tipo_logradouro": "Avenida",
                "bairro": "Morumbi",
                "cidade": "Sao Paulo",
                "cep": "01000",
                "tipo": "apartamento",
                "valor": 100000,
                "data_aquisicao": "2026-09-08"
            }
    response = client.put("/imoveis/2001", json=payload)

    assert response.status_code == 404
    assert response.get_json() == {"erro":"Imovel não encontrado"}

    mock_cursor.execute.assert_called_once_with('UPDATE imoveis SET logradouro = %s, tipo_logradouro = %s, bairro = %s, cidade = %s, cep = %s, tipo = %s, valor = %s, data_aquisicao = %s WHERE id = %s',
                                             ('Panamby','Avenida','Morumbi','Sao Paulo','01000','apartamento',100000,'2026-09-08', 2001),)
    mock_conn.commit.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()

@patch("api.conectar_banco")
def test_atualizar_imovel_erro_validacao(mock_conectar_banco, client):
    response = client.put("/imoveis/1", json={"logradouro": "Morumbi"})

    assert response.status_code == 400
    assert response.get_json() == {"erro": "Campos obrigatórios: logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao"}

    mock_conectar_banco.assert_not_called()

@patch('api.conectar_banco')
def test_delete_imovel_ok(mock_conectar_banco,client):

    mock_con = MagicMock()
    mock_cur = MagicMock()

    mock_con.cursor.return_value = mock_cur

    mock_cur.rowcount = 1  
    mock_conectar_banco.return_value = mock_con

    response = client.delete('/imoveis/1',
            json = {
                "logradouro": "Panamby",
                "tipo_logradouro": "Avenida",
                "bairro": "Morumbi",
                "cidade": "Sao Paulo",
                "cep": "01000",
                "tipo": "apartamento",
                "valor": 100000,
                "data_aquisicao": "2026-09-08"
            })

    assert response.status_code == 200
    assert response.get_json() == {"mensagem": "Imovel excluída com sucesso"}

    mock_cur.execute.assert_called_once_with("DELETE FROM imoveis WHERE id = %s",(1,))

    mock_con.commit.assert_called_once()
    mock_cur.close.assert_called_once()
    mock_con.close.assert_called_once()

@patch('api.conectar_banco')
def test_delete_imovel_erro(mock_conectar_banco, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.rowcount = 0
    mock_conectar_banco.return_value = mock_conn

    response = client.delete("/imoveis/5000")

    assert response.status_code == 404
    assert response.get_json() == {"erro": "Imovel não encontrado"}

    mock_cursor.execute.assert_called_once_with(
        "DELETE FROM imoveis WHERE id = ?",
        (5000,),
    )
    mock_conn.commit.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()
