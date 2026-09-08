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