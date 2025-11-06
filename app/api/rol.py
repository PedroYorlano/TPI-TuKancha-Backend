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
    try:
        rol = rol_service.get_by_id(id)
        if rol is None:
            return jsonify({"error": "Rol no encontrado"}), 404
        return jsonify(rol_schema.dump(rol))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Crear un nuevo rol
@bp_rol.post('/')
def crear_rol():
    data = request.get_json()
    try:
        rol = rol_service.create(data)
        return jsonify(rol_schema.dump(rol)), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Error al crear el rol"}), 500

# Actualizar un rol por su ID
@bp_rol.put('/<int:id>')
def actualizar_rol(id):
    data = request.get_json()
    try:
        rol = rol_service.update(id, data)
        return jsonify(rol_schema.dump(rol)), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": "Error al actualizar el rol"}), 500

# Eliminar un rol por su ID
@bp_rol.delete('/<int:id>')
def eliminar_rol(id):
    try:
        rol_service.delete(id)
        return '', 204 
    except ValueError as e:
        return jsonify({"error": "Rol no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
