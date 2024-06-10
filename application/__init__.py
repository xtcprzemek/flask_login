from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

#initialize extensions
login = LoginManager() 
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('flask.py')
    with app.app_context():
        # Adding components
        initialize_extensions(app)
        # Adding blueprints
        register_blueprints(app)
    return app
def initialize_extensions(app):
    login.init_app(app)
    login.login_view = 'bp.login'
    db.init_app(app)
    migrate.init_app(app, db)

def register_blueprints(app):
    from application.views import bp
    app.register_blueprint(bp)