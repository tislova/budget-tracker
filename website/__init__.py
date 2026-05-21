from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
from os import path
from flask_login import LoginManager, user_unauthorized

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-fallback-key-not-for-production')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    app.static_folder = 'static'

    from .views import views
    from .auth import auth
    from .models import User, Transaction

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    
    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.unauthorized_handler
    def unauthorized_callback():
        return redirect(url_for('auth.login'))


    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
