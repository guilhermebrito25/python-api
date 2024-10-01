#imports FLask
from flask import Flask, jsonify, request

#imports SQLalchemy
from sqlalchemy import create_engine, Column, String, Integer, select
from sqlalchemy.orm import sessionmaker, declarative_base

#imports JWT Token
import jwt
from datetime import datetime, timedelta

#imports PWD lib de hash senhas
from pwdlib import PasswordHash


#Cria função recomendada hash senhas
password_hash = PasswordHash.recommended()


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
    password = Column("password", String(150))
    
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

def msg(msg):
    print('-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-')
    print(msg)
    print('-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-')


#CRUD
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
#CREAT
#CRIA UM UNICO USUARIO
@app.route('/usuario/creat', methods=['POST'])
def criar_usuario():
    dados_usuario = request.get_json()
    consulta_usuario = session.query(Usuario).filter_by(login=dados_usuario.get('login')).first()  
    try:
        if consulta_usuario.login == dados_usuario.get('login'):
            return jsonify('usuario ja existe')
    except:
        usuario = Usuario(nome = dados_usuario.get('nome'), login = dados_usuario.get('login'), password = password_hash.hash(dados_usuario.get('password')))
        session.add(usuario)
        session.commit()
        return jsonify(dados_usuario)


#READ
#ENRTREGA A LISTA DE USUARIOS COMPLETA COM NOME E LOGIN DO USUARIO 
@app.route('/usuario/read/all', methods=['GET'])
def pegar_usuarios():
    usuarios = session.query(Usuario)
    usuariosL = []
    for user in usuarios:
        usuariosD = { 'id': user.id, 'nome': user.nome}
        usuariosL.append(usuariosD)
    return jsonify(usuariosL)


#ENTREGA UM USUARIO ESPECIFICO - Apartir do ID
@app.route('/usuario/read/<int:ide>', methods=['GET'])
def pegar_usuario(ide):
    try: 
        usuario = session.query(Usuario).filter_by(id=ide).first()
        return jsonify(usuario.nome)
    except:
        return jsonify('USUARIO NAO EXISTE')
    
#login
@app.route('/login', methods=['POST'])
def login():
    dadosLogin = request.get_json()
     
    try:
        usuarioLogin = session.query(Usuario).filter_by(login = dadosLogin.get('login')).first()
        if dadosLogin.get('login') == usuarioLogin.login and password_hash.verify(dadosLogin.get('password'),  usuarioLogin.password):
            return jsonify('User open')
        else:
            return jsonify('User hfhf find')
    except:
        return jsonify('User not find')

app.run(port=3000, host='localhost', debug=True)