from flask_wtf import FlaskForm
from flask_wtf.file import FileField, file_allowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from comunidadebutterfly.models import Usuario
from flask_login import current_user

class Login(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    lembrar_usuario = BooleanField('Lembrar Usuário')
    botao_login = SubmitField('Login')

class CriarConta(FlaskForm):
    user = StringField('Username', validators=[DataRequired(), Length(3, 18)])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    confirmacao_senha = PasswordField('Confirmar Senha', validators=[DataRequired(), EqualTo('senha')])
    botao_cadastro = SubmitField('Criar Conta')


    # validate_on_submit nos routes roda todas as validações e qualquer função na classe que comece 
    # com validate_, então essa função serve para verificar se o email já existe no banco de dados
    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('Email já cadastrado. Tente novamente!')
        
    def validate_user(self, user):
        usuario = Usuario.query.filter_by(username=user.data).first()
        if usuario:
            raise ValidationError('Usuário já cadastrado. Tente novamente!')

class EditarPerfil(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(3, 18)])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    foto_perfil = FileField('Foto de Perfil', validators=[file_allowed(['png', 'jpg'])])
    botao_salvar = SubmitField('Salvar')

    def validate_email(self, email):
        if current_user.email != email.data:
            usuario = Usuario.query.filter_by(email=email.data).first()
            if usuario:
                raise ValidationError('Email já cadastrado. Tente novamente!')
            
    def validate_username(self, username):
        if current_user.username != username.data:
            usuario = Usuario.query.filter_by(username=username.data).first()
            if usuario:
                raise ValidationError('Usuário já cadastrado. Tente novamente!')
            
class CriarPost(FlaskForm):
    titulo = StringField('Título', validators=[DataRequired(), Length(3, 100)])
    corpo = TextAreaField('Corpo', validators=[DataRequired()])
    botao_criarpost = SubmitField('Enviar')