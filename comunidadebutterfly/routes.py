from comunidadebutterfly import app, database, bcrypt
from comunidadebutterfly.forms import Login, CriarConta, EditarPerfil, CriarPost
from comunidadebutterfly.models import Usuario, Post
from flask import render_template, url_for, redirect, flash, request, abort
from flask_login import login_user, logout_user, current_user, login_required
from secrets import token_hex
from PIL import Image
import os


@app.route("/Comunidade")
def home_page():
    posts = Post.query.order_by(Post.id.desc())
    return render_template('home.html', posts=posts)

@app.route("/Comunidade/Contatos")
@login_required
def contatos():
    return render_template('contatos.html')

@app.route("/Comunidade/Usuarios")
@login_required
def usuarios():
    lista_usuarios = Usuario.query.all()
    dic = {}
    for usuario in lista_usuarios:
        dic[usuario] = 0
    posts = Post.query.all()
    for post in posts:
        dic[post.autor] += 1

    return render_template('usuarios.html', lista_usuarios=lista_usuarios, dic=dic)

@app.route("/Comunidade/Login", methods=['GET', 'POST'])
def login():
    form_login = Login()

    # validação so usuário para fazer login
    if form_login.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form_login.email.data).first() # pegando o usuario
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data): # verificando se existe
            login_user(usuario, remember = form_login.lembrar_usuario.data) # fazendo login com o login_user

            # rediricionamento automático
            parametro_next = request.args.get('next')
            if parametro_next: # se a página de login está sendo acessada da solicitação de outra pg
                return redirect(parametro_next)
            else:
             return redirect(url_for('home_page'))
            
        else:
            flash('E-mail ou senha inválidos. Tente novamente!', 'alert-danger')

    return render_template('login.html', form_login=form_login)

@app.route("/Comunidade/Cadastro", methods=['GET', 'POST'])
def cadastro():
    form_cadastro = CriarConta()

    # adicionando usuário no banco de dados
    if form_cadastro.validate_on_submit():
        senha_cript = bcrypt.generate_password_hash(form_cadastro.senha.data)

        usuario = Usuario(username=form_cadastro.user.data, email=form_cadastro.email.data, senha=senha_cript)
        database.session.add(usuario)
        database.session.commit()

        return redirect(url_for('home_page'))
    return render_template('cadastro.html', form_cadastro=form_cadastro)

@app.route("/Comunidade/Post/Criar", methods=['GET', 'POST'])
@login_required
def criar_post():
    form_post = CriarPost()
    if form_post.validate_on_submit():
       post = Post(titulo=form_post.titulo.data, corpo=form_post.corpo.data, autor=current_user)
       database.session.add(post)
       database.session.commit()
       return redirect(url_for('home_page'))
    return render_template('post+.html', form_post=form_post)

@app.route("/Comunidade/Perfil")
@login_required
def perfil_user():
    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.foto_perfil))
    posts_user = Post.query.filter_by(autor=current_user)

    posts = Post.query.order_by(Post.id.desc())
    ultimo_post = ' '
    for post in posts:
        if post.autor == current_user:
            ultimo_post = post
            break

    return render_template('perfil.html', foto_perfil=foto_perfil, posts_user=posts_user, ultimo_post=ultimo_post)

def salvar_imagem(imagem):
    codigo = token_hex(8)
    nome, extensao = os.path.splitext(imagem.filename)
    nome_arquivo = nome + codigo + extensao
    caminho = os.path.join(app.root_path, 'static/fotos_perfil', nome_arquivo)
    
    tamanho = (200, 200)
    imagem_reduzida = Image.open(imagem)
    imagem_reduzida.thumbnail(tamanho)
    imagem_reduzida.save(caminho)
    return nome_arquivo

@app.route("/Comunidade/Perfil/Editar", methods=['GET', 'POST'])
@login_required
def editar_perfil():
    perfil = EditarPerfil()
    if perfil.validate_on_submit():
        current_user.email = perfil.email.data
        current_user.username = perfil.username.data
        if perfil.foto_perfil.data:
            nome_imagem = salvar_imagem(perfil.foto_perfil.data)
            current_user.foto_perfil = nome_imagem
        database.session.commit()
        return redirect(url_for('perfil_user'))
    
    elif request.method == 'GET':
        perfil.username.data = current_user.username
        perfil.email.data = current_user.email

    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.foto_perfil))
    return render_template('editar_perfil.html', foto_perfil=foto_perfil, perfil=perfil)

@app.route("/Comunidade/Perfil/Sair")
def sair():
    logout_user()
    return redirect(url_for('home_page'))

@app.route('/Comunidade/Post/<post_id>')
def post(post_id):
    post = Post.query.get(post_id)
    return render_template('post.html', post=post)

@app.route('/Comunidade/Post/Excluir<post_id>')
@login_required
def excluir_post(post_id):
    post = Post.query.get(post_id)
    if post.autor.email == current_user.email:
        database.session.delete(post)
        database.session.commit()
        return redirect(url_for('home_page'))
    else:
        abort(403)

@app.route('/Comunidade/Post/Editar<post_id>', methods=['GET', 'POST'])
@login_required
def editar_post(post_id):
    form_post = CriarPost()
    post = Post.query.get(post_id)
    if request.method == 'GET':
        form_post.titulo.data = post.titulo
        form_post.corpo.data = post.corpo
    elif form_post.validate_on_submit():
        post.titulo = form_post.titulo.data
        post.corpo = form_post.corpo.data
        database.session.commit()
        return redirect(url_for('home_page'))
    return render_template('postedit.html', form_post=form_post)