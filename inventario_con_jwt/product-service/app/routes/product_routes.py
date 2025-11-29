from flask import Blueprint, jsonify, request
from app import db
from app.models.product import Producto
from app.services.auth_middleware import require_jwt

# Sin url_prefix, todo el path completo
product_bp = Blueprint("products", __name__)

# 1) Listar productos (cualquier usuario autenticado)
@product_bp.route("/products", methods=["GET"])
@require_jwt()
def listar_productos():
    productos = Producto.query.all()
    data = []
    for p in productos:
        data.append({
            "id": p.id,
            "nombre": p.nombre,
            "descripcion": p.descripcion,
            "precio": float(p.precio),
            "stock": p.stock
        })
    return jsonify(data), 200


# 2) Estadisticas simples (tambien solo autenticados)
@product_bp.route("/products/stats", methods=["GET"])
@require_jwt()
def stats_productos():
    total = Producto.query.count()
    return jsonify({"total_productos": total}), 200


# 3) Crear producto (solo ADMIN y EDITOR)
@product_bp.route("/products", methods=["POST"])
@require_jwt(roles=["ADMIN", "EDITOR"])
def crear_producto():
    data = request.get_json() or {}
    nombre = data.get("nombre")
    precio = data.get("precio")
    descripcion = data.get("descripcion")
    stock = data.get("stock", 0)

    if not nombre or precio is None:
        return jsonify({"message": "nombre y precio son obligatorios"}), 400

    producto = Producto(
        nombre=nombre,
        descripcion=descripcion,
        precio=precio,
        stock=stock
    )
    db.session.add(producto)
    db.session.commit()

    return jsonify({"message": "producto creado", "id": producto.id}), 201


# 4) Actualizar producto (solo ADMIN y EDITOR)
@product_bp.route("/products/<int:product_id>", methods=["PUT"])
@require_jwt(roles=["ADMIN", "EDITOR"])
def actualizar_producto(product_id):
    producto = Producto.query.get_or_404(product_id)
    data = request.get_json() or {}

    if "nombre" in data:
        producto.nombre = data["nombre"]
    if "descripcion" in data:
        producto.descripcion = data["descripcion"]
    if "precio" in data:
        producto.precio = data["precio"]
    if "stock" in data:
        producto.stock = data["stock"]

    db.session.commit()
    return jsonify({"message": "producto actualizado"}), 200


# 5) Eliminar producto (solo ADMIN)
@product_bp.route("/products/<int:product_id>", methods=["DELETE"])
@require_jwt(roles=["ADMIN"])
def eliminar_producto(product_id):
    producto = Producto.query.get_or_404(product_id)
    db.session.delete(producto)
    db.session.commit()
    return jsonify({"message": "producto eliminado"}), 200
