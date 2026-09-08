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
    cursor.execute("SELECT id, logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao FROM imoveis WHERE id = %s", (id,))
    resultado = cursor.fetchone()
    conexao.close()
    cursor.close()
    if resultado is None:
        return jsonify({"erro": "Imoveis não encontrado"}), 404
    imoveis = {'id': resultado[0], 'logradouro': resultado[1], 'tipo_logradouro': resultado[2], 'bairro': resultado[3], 'cidade': resultado[4], 'cep': resultado[5], 'tipo': resultado[6], 'valor': resultado[7], 'data_aquisicao': resultado[8]}
    return imoveis, 200

@app.route('/imoveis',methods=['POST'])
def adiciona_imovel():
    imovel  = request.get_json()

    if not imovel or not all(campo in imovel for campo in ['logradouro','tipo_logradouro','bairro','cidade','cep','tipo','valor','data_aquisicao']):
       return jsonify({'erro':'Campos obrigatórios: logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao'}),400 


    con = conectar_banco()
    cur = con.cursor()
    cur.execute(
        "INSERT INTO imoveis (logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                (imovel['logradouro'],imovel['tipo_logradouro'],imovel['bairro'],imovel['cidade'],imovel['cep'],imovel['tipo'],imovel['valor'],imovel['data_aquisicao']),
    )

    con.commit()

    id_imovel = cur.lastrowid

    cur.close()
    con.close()

    return jsonify({'id':id_imovel}),201

@app.route('/imoveis/<int:id>',methods=['PUT'])
def update_imovel(id):

    dados = request.get_json()

    if not dados or not all(campo in dados for campo in ['logradouro','tipo_logradouro','bairro','cidade','cep','tipo','valor','data_aquisicao']):
        return jsonify({'erro':'Campos obrigatórios: logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao'}),400

    con = conectar_banco()
    cur = con.cursor()
    cur.execute('UPDATE imoveis SET logradouro = %s, tipo_logradouro = %s, bairro = %s, cidade = %s, cep = %s, tipo = %s, valor = %s, data_aquisicao = %s WHERE id = %s',
                                             ('Panamby','Avenida','Morumbi','Sao Paulo','01000','apartamento',100000,'2026-09-08',id,))

    con.commit()

    if cur.rowcount == 0 :
        cur.close()
        con.close()
        return jsonify({'erro':'Imovel não encontrado'}),404
    
    cur.close()
    con.close()

    return jsonify({'mensagem':'Imovel atualizado com sucesso'}),200

if __name__ == '__main__':
    app.run(debug=True)