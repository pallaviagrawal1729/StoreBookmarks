import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config['SECRET_KEY'] = b"\xb9'*_\xaa\xc7\x13\xfd\xab\x17\xd5m*\xbe\xf2\xb1\xa7!\xbcdf\xa5\xfa\xba"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'bookmarkProject.db')
app.config['DEBUG'] = True
db = SQLAlchemy(app)

#Configure authentication
login_manager = LoginManager()
login_manager.session_protection="strong"
login_manager.login_view = "login"
login_manager.init_app(app)

from bookmarkProject import model
from bookmarkProject import views
