from importlib.abc import FileLoader

from email_validator import validate_email
from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, length, ValidationError, data_required
from comunidadeimpressionadora.models import Usuario
from flask_login import current_user
from flask_wtf.file import FileField,FileAllowed

class FormCriarConta(FlaskForm):
    username = StringField('Nome de usuario', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), length(6,25)])
    confirmacao_senha = PasswordField('Confirmação da Senha', validators=[DataRequired(), EqualTo('senha')])
    botao_submit_criarconta = SubmitField('Criar Conta')

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError(f'O Email inserido {email.data} já foi utilizado, informe um outro email par cadastro')


class FormLogin(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6,25)])
    lembrar_dados = BooleanField('Lembrar dados de acesso')
    botao_submit_login = SubmitField('Fazer Login')


class FormEditarPerfil(FlaskForm):
    username= StringField('Nome de usuario', validators=[DataRequired()])
    email= StringField('E-mail', validators=[DataRequired(), Email()])
    foto_perfil =  FileField('Atualizar foto de perfil', validators=[FileAllowed(['jpg', 'png'])])

    curso_excel = BooleanField(' - Curso Excel - ')
    curso_PowerBI = BooleanField(' - Curso PowerBI - ')
    curso_Python = BooleanField(' - Curso Python - ')
    curso_Office = BooleanField(' - Curso Office - ')
    curso_Outlook = BooleanField(' - Curso Outlook - ')
    curso_PowerPoint = BooleanField(' - Curso PowerPoint - ')


    botao_submit_editarperfil= SubmitField('Confirmar Edição')

    def validate_email(self, email):
        # Só consulta o banco se o email foi alterado
        if current_user.email != email.data:
            usuario = Usuario.query.filter_by(email=email.data).first()
            if usuario:
                raise ValidationError(
                    f'O Email inserido {email.data} já existe, informe outro email válido para cadastro')


class FormCriarPost(FlaskForm):
    titulo = StringField('Titulo do Post', validators=[DataRequired(), Length(2,140)])
    corpo = TextAreaField('Escreva seu post aqui!', validators=[data_required()])
    botao_submit = SubmitField('Criar Post')