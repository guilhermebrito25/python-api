from flask import Flask, jsonify, request

app = Flask(__name__)

livros = [
    {   
        'id': 1,
        'livro': 'Pedra filosofal',
        'autor': 'Kleber BamBam'
    },
    {
        'id': 2,
        'livro': 'Uma estrela no ceu',
        'autor': 'JuniorBaiano'
    },
    {   
        'id': 3,
        'livro': 'O menino emdemoiado',
        'autor': 'Popó mão de ferro'
    }
]

#Pega todos os livros - 
@app.route('/livros', methods=['GET'])
def pegarLivros():
    return jsonify(livros)

#Pega um livro por ID
@app.route('/livros/<int:id>', methods=['GET'])
def pegarLivroId(id):
    for c in livros:
        if c.get('id') == id:
            return jsonify(c)

#Edita um livro por ID
@app.route('/livros/<int:id>', methods=['PUT'])
def editaLivroId(id):
    livroAlterado = request.get_json()
    for i,l in enumerate(livros):
        if l.get('id') == id:
            livros[i].update(livroAlterado)
            return jsonify(livros[i])
        

    



app.run(port=3000, host='localhost', debug=True)