import pytest
from unittest.mock import patch, MagicMock
from api import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

@patch("api.conectar_banco")
def test_listar_imoveis_com_dados(mock_conectar_banco, client):
    """GET /contacts - lista com dados."""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [(1, 'Panamby', 'Avenida', 'Morumbi', 'Sao Paulo', '01000', 'apartamento', 100000, '2026-09-08')]

    mock_conectar_banco.return_value = mock_conn

    response = client.get("/imoveis")

    assert response.status_code == 200
    assert response.get_json() == [
        {'id': 1,
          'logradouro': 'Panamby',
            'tipo_logradouro': 'Avenida',
              'bairro': 'Morumbi',
                'cidade': 'Sao Paulo',
                  'cep': '01000',
                    'tipo': 'apartamento',
                        'valor': 100000,
                            'data_aquisicao': '2026-09-08'}]

    mock_cursor.execute.assert_called_once_with(
        "SELECT id, logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao FROM imoveis"
    )
    mock_cursor.fetchall.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()