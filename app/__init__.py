from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = "auth.login"


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    from app.routes import (
        auth_bp,
        pacientes_bp,
        actividad_fisica_bp,
        actividad_social_bp,
        historial_clinico_bp,
    )

    app.register_blueprint(auth_bp)
    app.register_blueprint(pacientes_bp)
    app.register_blueprint(actividad_fisica_bp)
    app.register_blueprint(actividad_social_bp)
    app.register_blueprint(historial_clinico_bp)

    return app