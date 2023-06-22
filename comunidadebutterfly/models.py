from comunidadebutterfly import database, login_manager
from datetime import datetime
from flask_login import UserMixin


# pega o usuário no banco de dados através da sua chave primária
@login_manager.user_loader
def getar_user(id_usuario):
    return Usuario.query.get(int(id_usuario))


class Usuario(database.Model, UserMixin): # UserMixin -> Passar as características necessárias para o login
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String, nullable=False, unique=True)
    email = database.Column(database.String, nullable=False, unique=True)
    senha = database.Column(database.String, nullable=False)
    foto_perfil = database.Column(database.String, default='fotopadrao.jpg')
    posts = database.relationship('Post', backref='autor', lazy=True)  # relacionamento com a classe abaixo

    def contar_posts(self):
        return len(self.posts)
    
class Post(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    titulo = database.Column(database.String, nullable=True)
    corpo = database.Column(database.Text, nullable=True)
    data_criacao = database.Column(database.DateTime, default=datetime.utcnow)
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)