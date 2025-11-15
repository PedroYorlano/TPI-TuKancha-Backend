from flask import Blueprint, jsonify, request
from app import db
from app.services.rol_service import RolService
from app.schemas.rol_schema import rol_schema, roles_schema

bp_rol = Blueprint("rol", __name__, url_prefix="/api/v1/roles")

rol_service = RolService(db)


# Listar todos los roles
@bp_rol.get('/')
def listar_roles():
    roles = rol_service.get_all()
    return jsonify(roles_schema.dump(roles))
    
# Obtener un rol por su ID
@bp_rol.get('/<int:id>')
def obtener_rol(id):
    rol = rol_service.get_by_id(id)
    return jsonify(rol_schema.dump(rol))

# Crear un nuevo rol
@bp_rol.post('/')
def crear_rol():
    data = request.get_json()
    rol = rol_service.create(data)
    return jsonify(rol_schema.dump(rol)), 201

# Actualizar un rol por su ID
@bp_rol.put('/<int:id>')
def actualizar_rol(id):
    data = request.get_json()
    rol = rol_service.update(id, data)
    return jsonify(rol_schema.dump(rol)), 200

# Eliminar un rol por su ID
@bp_rol.delete('/<int:id>')
def eliminar_rol(id):
    rol_service.delete(id)
    return jsonify({"message": "Rol eliminado exitosamente"}), 200

