from flask import Blueprint, jsonify, request
from app import db
from app.services.rol_service import RolService
from app.services.user_service import UserService
from app.schemas.user_schema import user_schema, users_schema, user_create_schema

bp_user = Blueprint("user", __name__, url_prefix="/api/v1/users")

user_service = UserService(db)

@bp_user.get('/')
def listar_usuarios():
    usuarios = user_service.get_all()
    # Se usa 'users_schema' para formatear la SALIDA
    return jsonify(users_schema.dump(usuarios))

@bp_user.get('/<int:id>')
def obtener_usuario(id):
    try:
        usuario = user_service.get_by_id(id)
        if usuario is None:
            return jsonify({"error": "Usuario no encontrado"}), 404
        return jsonify(user_schema.dump(usuario))
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp_user.post('/')
def crear_usuario():
    data = request.get_json()
    print("Received data:", data)
    errors = user_create_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    try:
        # El servicio crea el usuario (con el hashing)
        nuevo_usuario = user_service.create(data)
        
        # Se devuelve la SALIDA formateada con 'user_schema' (sin password)
        return jsonify(user_schema.dump(nuevo_usuario)), 201
        
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": "Error al crear el usuario"}), 500

@bp_user.patch('/<int:id>')
def actualizar_usuario(id):
    data = request.get_json()
    errors = user_create_schema.validate(data, partial=True)
    if errors:
        return jsonify(errors), 400

    try:
        usuario = user_service.update(id, data)
        return jsonify(user_schema.dump(usuario)), 200
    except ValueError as e:
        return jsonify({"error": "Usuario no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": "Error al actualizar el usuario"}), 500

@bp_user.delete('/<int:id>')
def eliminar_usuario(id):
    data = request.get_json()
    errors = user_create_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    
    try:
        user_service.delete(id)
        return '', 204 
    except ValueError as e:
        return jsonify({"error": "Usuario no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

