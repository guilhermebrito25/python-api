from flask import Flask, jsonify, request

from sqlalchemy import create_engine, String
from sqlalchemy.orm import declarative_base, Mapped, mapped_column


##CRIAÇÃO FUNÇÃO CONEXÃO COM O BD - ALCHEMYSQL
engine = create_engine("mysql+mysqldb://root:1234@localhost:3306/crm2", echo=True)


##CRIANDO AS COLUNAS NO BANCO DE DADOS - 
base = declarative_base()
class Usuario(base): #classe criadora "base declarativa" - 
    __tablename__ = 'usuarios' #nome da tabela
    
    id: Mapped[int] = mapped_column(primary_key=True) #OBRIGATORIO - 
    name: Mapped[str] = mapped_column(String(30))
    login: Mapped[str] = mapped_column(String(20))
    password: Mapped[str] = mapped_column(String(20))
base.metadata.create_all(engine) #CRIAÇÃO LITERAL DAS TABELAS NO BANCO


##CRIAÇÃO FUNÇÃO APP DO FLASK
app = Flask(__name__)


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