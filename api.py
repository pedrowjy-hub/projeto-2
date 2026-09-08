from flask import Flask, request, jsonify 
from database import conectar_banco

app = Flask(__name__)

@app.route('/imoveis', methods = ['GET'])
def listar_imoveis():
    con = conectar_banco()
    cur = con.cursor()

    cur.execute('SELECT id, logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao FROM imoveis')

    resultado = [
        {
            'id': imovel[0],
            'logradouro': imovel[1],
            'tipo_logradouro': imovel[2],
            'bairro': imovel[3],
            'cidade': imovel[4],
            'cep': imovel[5],
            'tipo': imovel[6],
            'valor': imovel[7],
            'data_aquisicao': imovel[8]
        }
        for imovel in cur.fetchall()
    ]

    cur.close()
    con.close()

    return jsonify(resultado), 200

@app.route('/imoveis/<int:id>', methods=['GET'])
def obter_imovel(id):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute("SELECT id, logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao FROM imoveis WHERE id = ?", (id,))
    resultado = cursor.fetchone()
    conexao.close()
    cursor.close()
    if resultado is None:
        return jsonify({"erro": "Imoveis não encontrado"}), 404
    imoveis = {'id': resultado[0], 'logradouro': resultado[1], 'tipo_logradouro': resultado[2], 'bairro': resultado[3], 'cidade': resultado[4], 'cep': resultado[5], 'tipo': resultado[6], 'valor': resultado[7], 'data_aquisicao': resultado[8]}
    return imoveis, 200