import os
from datetime import timedelta

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

db_type = os.getenv('WEB_DB', 'sqlite')
if db_type == 'postgresql':
    user = os.getenv('PG_USER')
    password = os.getenv('PG_PASSWORD')
    ip = os.getenv('PG_IP')
    port = os.getenv('PG_PORT', '5432')
    database_name = os.getenv('PG_DATABASE')
    schema = os.getenv('PG_SCHEMA')

db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()


def create_app():
    app = Flask(__name__, template_folder='templates')
    app.config['SECRET_KEY'] = "Debug_HBJgfvkjghu78yuuhigvhj87ty9"
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    app.config['PERMANENT_COOKIE_SESSION'] = timedelta(days=10)

    if db_type == 'postgresql':
        app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{user}:{password}@{
            ip}:{port}/{database_name}?options=-c%20search_path={schema}'
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./db.sqlite'

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    # import blueprints here
    from app.blueprints.core.routes import core
    from app.blueprints.auth.routes import auth

    app.register_blueprint(core, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/auth')

    migrate = Migrate(app, db)

    return app
