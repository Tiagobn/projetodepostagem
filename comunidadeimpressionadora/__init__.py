from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__)


app.config['SECRET_KEY'] = 'a8r,yewU%srHU[(e'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comunidade.db'


database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'alert-warning'
from comunidadeimpressionadora import routes