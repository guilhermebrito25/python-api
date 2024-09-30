
from flask import Flask, jsonify, request
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import sessionmaker, declarative_base

#cria o router do flask
app = Flask(__name__)

#conecta o alchemy no BD
engine = create_engine("mysql+mysqldb://root:1234@localhost:3306/crm3", echo=True)

#inicia seção, onde será usado os metodos CRUD
Session = sessionmaker(bind=engine)
session = Session()


#inicia a "schame" e criação da estrura do BD com as tabelas(usuarios e livros)
Base = declarative_base()

#usuarios
class Usuario(Base):
    __tablename__= 'usuarios'

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    nome = Column("nome", String(50))
    login = Column("login", String(20))
    password = Column("password", String(20))
    
    def __init__(self, nome, login, password):
        self.nome = nome
        self.login = login
        self.password = password

#livros
class Livro(Base):
    __tablename__= 'livros'

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    titulo = Column("titulo", String(50))
    autor = Column("autor", String(50))
    resumo = Column("resumo", String(150))

    def __init__(self, titulo, autor, resumo):
        self.titulo = titulo
        self.autor = autor
        self.resumo = resumo
    
Base.metadata.create_all(bind=engine)


#CRUD
#CRIAR
@app.route('/usuario/add', methods=['POST'])
def criar_usuario():
    dados_usuario = request.get_json()
    consulta_usuario = session.query(Usuario).filter_by(login=dados_usuario.get('login')).first()
    
    try:
        if consulta_usuario.login == dados_usuario.get('login'):
            return jsonify('usuario ja existe')

    except:
        usuario = Usuario(nome=dados_usuario.get('nome'), login=dados_usuario.get('login'), password=dados_usuario.get('password'))
        session.add(usuario)
        session.commit()
        return jsonify(dados_usuario)
    

app.run(port=3000, host='localhost', debug=True)

     
# #ADICIONA UM NOVO USUARIO
# @app.route('/user/new', methods=['POST'])
# def addUser ():
#     user = request.get_json()
    
#     nameAdd = user.get('name')
#     loginAdd = user.get('login')
#     passwordAdd = user.get('password')
#     userAdd = Usuario(name=nameAdd,login=loginAdd,password=passwordAdd)
   
#     return (f'Usuario adicionado')
        


