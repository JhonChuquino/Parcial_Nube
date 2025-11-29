from functools import wraps
from flask import request, jsonify, g
import os
import requests

# URL interna del servicio de autenticacion
AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "http://auth-service:5001")


def require_jwt(roles=None):
    """
    roles: lista de roles permitidos, ejemplo ["ADMIN", "EDITOR"].
    Si es None, solo valida que haya token correcto.
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            auth_header = request.headers.get("Authorization", "")
            parts = auth_header.split()

            if len(parts) != 2 or parts[0].lower() != "bearer":
                return jsonify({"message": "Token no proporcionado"}), 401

            token = parts[1]

            # Llamar a auth-service para validar el token
            try:
                resp = requests.post(
                    f"{AUTH_SERVICE_URL}/auth/validate",
                    json={"token": token},
                    timeout=3
                )
            except requests.RequestException:
                return jsonify({"message": "No se pudo contactar al servicio de autenticacion"}), 503

            if resp.status_code != 200:
                # auth-service ya indica que el token es invalido
                return jsonify({"message": "Token invalido"}), 401

            data = resp.json()
            if not data.get("valid"):
                return jsonify({"message": "Token invalido"}), 401

            payload = data.get("payload", {})

            # guardar datos del usuario en el contexto de la request
            g.current_user_id = payload.get("sub")
            g.current_username = payload.get("username")
            g.current_role = payload.get("role")

            if roles and g.current_role not in roles:
                return jsonify({"message": "No tienes permisos para esta accion"}), 403

            return fn(*args, **kwargs)
        return wrapper
    return decorator
