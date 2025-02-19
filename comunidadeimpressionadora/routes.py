from ftplib import all_errors
from importlib.metadata import pass_none

from flask import render_template, redirect, url_for, flash, request, abort
from comunidadeimpressionadora import app, database, bcrypt
from comunidadeimpressionadora.forms import FormLogin, FormCriarConta, FormEditarPerfil, FormCriarPost
from comunidadeimpressionadora.models import Usuario, Post
from comunidadeimpressionadora.models import database
from comunidadeimpressionadora.templates.so_teste import usuario
from flask_login import login_user, logout_user,current_user, login_required
import secrets
import os
from PIL import Image




@app.route("/")
def home():
    posts = Post.query.order_by(Post.id.desc())
    return  render_template('home.html', posts=posts)


@app.route('/contato')
def contato():
    return render_template('contato.html')


@app.route('/usuarios')
@login_required
def usuarios():
    lista_usuarios = Usuario.query.all()
    return render_template('usuarios.html', lista_usuarios=lista_usuarios)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form_login = FormLogin()
    form_criarconta = FormCriarConta()

    # Verifica se o formulário de login foi enviado
    if 'botao_submit_login' in request.form and form_login.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
            login_user(usuario, remember=form_login.lembrar_dados.data)
            flash(f'Login realizado com sucesso para o email: {form_login.email.data}', 'alert-success')
            parametro_next = request.args.get('next')
            if parametro_next:
                return redirect(parametro_next)
            return redirect(url_for('home'))
        else:
            flash('Falha de login: email ou senha incorretos', 'alert-danger')

    # Verifica se o formulário de criação de conta foi enviado
    if 'botao_submit_criarconta' in request.form and form_criarconta.validate_on_submit():
        # Criptografa a senha e cria o usuário
        senha_cript = bcrypt.generate_password_hash(form_criarconta.senha.data).decode('utf-8')
        usuario = Usuario(
            username=form_criarconta.username.data,
            email=form_criarconta.email.data,
            senha=senha_cript
        )
        database.session.add(usuario)
        database.session.commit()
        flash(f'Conta criada para o email {form_criarconta.email.data}', 'alert-success')
        return redirect(url_for('home'))

    # Caso algum formulário tenha erros de validação, exibe as mensagens
    if form_criarconta.errors:
        for campo, erros in form_criarconta.errors.items():
            for erro in erros:
                flash(f'Problemas no campo {campo}: {erro}', 'alert-danger')

    return render_template('login.html', form_login=form_login, form_criarconta=form_criarconta)

@app.route('/sair')
@login_required
def sair():
    logout_user()
    flash(f'Logout feito da melhor forma', 'alert-info')
    return redirect(url_for('home'))

@app.route ('/perfil')
@login_required
def perfil():
    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.foto_perfil))
    return render_template('perfil.html', foto_perfil=foto_perfil)

@app.route('/post/criar', methods=['GET', 'POST'])
@login_required
def criar_post():
    form = FormCriarPost()
    if form.validate_on_submit():
        post = Post(titulo=form.titulo.data, corpo=form.corpo.data, autor=current_user)
        database.session.add(post)
        database.session.commit()
        flash('Post criado com sucesso', 'alert-success')
        return redirect(url_for('home'))
    return render_template('criarpost.html', form=form)



# Salva uma imagem enviada pelo usuário:
# 1. Gera um nome único para o arquivo combinando o nome original com um código aleatório.
# 2. Redimensiona a imagem para 110x110 pixels.
# 3. Salva a imagem redimensionada no diretório 'static/fotos_perfil'.
# 4. Retorna o novo nome do arquivo para uso posterior (como salvar no banco de dados).

def salvar_imagem(imagem):
    codigo = secrets.token_hex(8)
    nome, extensao = os.path.splitext(imagem.filename)
    nome_arquivo = nome + codigo + extensao
    caminho_completo = os.path.join(app.root_path, 'static/fotos_perfil', nome_arquivo)
    tamanho = (350,350)
    imagem_reduzida = Image.open(imagem)
    imagem_reduzida.thumbnail(tamanho)
    imagem_reduzida.save(caminho_completo)
    return nome_arquivo


def atualizar_cursos(form):
    lista_cursos = []
    for campo in form:
        if 'curso' in campo.name:
            if campo.data:
                lista_cursos.append(campo.label.text)
    return ';'.join(lista_cursos)


@app.route('/perfil/editar', methods=['GET', 'POST'])
@login_required
def editar_perfil():
    form = FormEditarPerfil()
    if form.validate_on_submit():
        current_user.email = form.email.data
        current_user.username = form.username.data
        if form.foto_perfil.data:
            nome_imagem = salvar_imagem(form.foto_perfil.data)
            current_user.foto_perfil = nome_imagem
        current_user.cursos = atualizar_cursos(form)
        database.session.commit()
        flash(f'O seu perfil foi atulizado com sucesso! ', 'alert-success')
        return redirect(url_for('perfil'))
    elif request.method == "GET":
        form.email.data = current_user.email
        form.username.data = current_user.username
    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.foto_perfil))
    return render_template('editarperfil.html',foto_perfil=foto_perfil, form=form)


@app.route('/post/<post_id>', methods=['GET', 'POST'])
@login_required
def exibir_post(post_id):
    post = Post.query.get(post_id)
    if current_user == post.autor:
        form = FormCriarPost()
        if request.method == 'GET':
            form.titulo.data = post.titulo
            form.corpo.data = post.corpo
        elif form.validate_on_submit():
            post.titulo = form.titulo.data
            post.corpo = form.corpo.data
            database.session.commit()
            flash('Seu post foi atualizado com sucesso', 'alert-success')
            return redirect(url_for('home'))
    else:
        form = None
    return render_template('post.html', post=post, form=form)


@app.route('/post/<post_id>/excluir', methods=['GET', 'POST'])
@login_required
def excluir_post(post_id):
    post = Post.query.get(post_id)
    if current_user == post.autor:
        database.session.delete(post)
        database.session.commit()
        flash('post excluido com sucesso!', 'alert-danger')
        return redirect(url_for('home'))
    else:
        abort(403)
