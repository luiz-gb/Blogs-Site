from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = '9c1ec5a635ed4018cdf71d00a6421a0a'

if os.getenv('DATABASE_URL'):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bancodados.db'

database = SQLAlchemy(app)
bcrypt = Bcrypt()
login_manager = LoginManager(app)
login_manager.login_view = 'login' # quando o cara acessar uma página proibida, vai ser direcionado a fazer login
login_manager.login_message = 'Faça login para continuar!'
login_manager.login_message_category = 'alert-info' # categoria do alerta (classe bootstrap)

import comunidadebutterfly.routes