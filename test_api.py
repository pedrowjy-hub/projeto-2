import pytest
from unittest.mock import patch, MagicMock
from api import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

@patch('api.conectar_banco')
def test_lista_imoveis_vazios(mock_conectar_banco,client):

    mock_con = MagicMock()
    mock_cur = MagicMock()

    mock_con.cursor.return_value = mock_cur
    mock_cur.fetchall.return_value = []

    mock_conectar_banco.return_value = mock_con

    response = client.get('/imoveis')

    assert response.status_code == 200
    assert response.get_json() == []

    mock_cur.execute.assert_called_once_with('SELECT id, logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao FROM imoveis')

    mock_cur.fetchall.assert_called_once()
    mock_cur.close.assert_called_once()
    mock_con.close.assert_called_once()