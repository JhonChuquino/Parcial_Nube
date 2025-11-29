from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from .config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    CORS(app)

    # importar rutas
    from app.routes.auth_routes import auth_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")

    # importar modelos y crear tablas en la BD
    with app.app_context():
        from app.models.user import Usuario  # importa el modelo
        db.create_all()  # aqui se crea la tabla "usuarios"

    return app
