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
    
    
    # crear tablas
    with app.app_context():
        db.create_all()

    # IMPORTAR Y REGISTRAR BLUEPRINTS
    from app.routes.product_routes import product_bp
    app.register_blueprint(product_bp)

    # RUTA DE PRUEBA SIMPLE
    @app.route("/debug-routes")
    def debug_routes():
        # Esto te permite ver todas las rutas registradas
        rutas = [str(r) for r in app.url_map.iter_rules()]
        return "<br>".join(rutas)

    return app
