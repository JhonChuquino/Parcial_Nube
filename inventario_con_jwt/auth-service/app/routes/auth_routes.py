from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
import jwt

from app import db
from app.config import Config
from app.models.user import Usuario

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"message": "username y password son requeridos"}), 400

    # buscar usuario
    user = Usuario.query.filter_by(username=username).first()

    if not user:
        return jsonify({"message": "credenciales invalidas"}), 401

    if not user.check_password(password):
        return jsonify({"message": "credenciales invalidas"}), 401

    if not user.is_active:
        return jsonify({"message": "usuario inactivo"}), 403

    # payload del JWT
    payload = {
        "sub": str(user.id),
        "username": user.username,
        "role": user.role,
        "exp": datetime.utcnow() + timedelta(hours=2),
    }

    token = jwt.encode(payload, Config.JWT_SECRET_KEY, algorithm="HS256")

    return jsonify(
        {
            "access_token": token,
            "token_type": "Bearer",
            "role": user.role,
        }
    ), 200


@auth_bp.route("/validate", methods=["POST"])
def validate_token():
    """Endpoint para que otros microservicios validen un JWT."""
    data = request.get_json() or {}
    token = data.get("token")

    if not token:
        return jsonify({"valid": False, "error": "token requerido"}), 400

    try:
        payload = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=["HS256"])
        # opcional: aqui podrias verificar que el usuario exista, este activo, etc.
        return jsonify({"valid": True, "payload": payload}), 200
    except Exception as e:
        return jsonify({"valid": False, "error": str(e)}), 401
