from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from app import db
from app.auth.decorators import role_required
from app.services.rol_service import RolService
from app.services.user_service import UserService
from app.schemas.user_schema import user_schema, users_schema, user_create_schema

bp_user = Blueprint("user", __name__, url_prefix="/api/v1/users")

user_service = UserService(db)

@bp_user.get('/')
@jwt_required()
@role_required(['admin'])
def listar_usuarios():
    try:
        usuarios = user_service.get_all()
        # Se usa 'users_schema' para formatear la SALIDA
        return jsonify(users_schema.dump(usuarios)), 200
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": "Error al listar usuarios", "details": str(e)}), 500

@bp_user.get('/<int:id>')
@jwt_required()
@role_required(['admin'])
def obtener_usuario(id):
    try:
        usuario = user_service.get_by_id(id)
        if usuario is None:
            return jsonify({"error": "Usuario no encontrado"}), 404
        return jsonify(user_schema.dump(usuario)), 200
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": "Error al obtener usuario", "details": str(e)}), 500

@bp_user.get('/club/<int:club_id>')
@jwt_required()
@role_required(['admin'])
def obtener_usuarios_por_club(club_id):
    try:
        usuarios = user_service.get_by_club(club_id)
        return jsonify(users_schema.dump(usuarios)), 200
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": "Error al obtener usuarios del club", "details": str(e)}), 500


@bp_user.post('/')
@jwt_required()
@role_required(['admin'])
def crear_usuario():
    try:
        data = request.get_json()
        
        # Validar que se recibió JSON
        if not data:
            return jsonify({"error": "No se recibió ningún dato JSON"}), 400
        
        print("=" * 50)
        print("CREAR USUARIO - Datos recibidos:", data)
        
        # Validar schema
        errors = user_create_schema.validate(data)
        if errors:
            print("Errores de validación:", errors)
            return jsonify({"error": "Errores de validación", "details": errors}), 400

        # El servicio crea el usuario (con el hashing)
        nuevo_usuario = user_service.create(data)
        
        # Se devuelve la SALIDA formateada con 'user_schema' (sin password)
        resultado = user_schema.dump(nuevo_usuario)
        print("Usuario creado exitosamente:", resultado)
        print("=" * 50)
        return jsonify(resultado), 201
        
    except ValueError as e:
        print(f"ValueError: {str(e)}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        import traceback
        print("=" * 50)
        print("ERROR AL CREAR USUARIO:")
        print(f"Tipo de error: {type(e).__name__}")
        print(f"Mensaje: {str(e)}")
        traceback.print_exc()
        print("=" * 50)
        return jsonify({
            "error": "Error al crear el usuario", 
            "details": str(e),
            "type": type(e).__name__
        }), 500

@bp_user.patch('/<int:id>')
@jwt_required()
@role_required(['admin'])
def actualizar_usuario(id):
    try:
        data = request.get_json()
        
        # Validar que se recibió JSON
        if not data:
            return jsonify({"error": "No se recibió ningún dato JSON"}), 400
        
        print("=" * 50)
        print(f"ACTUALIZAR USUARIO {id} - Datos recibidos:", data)
        
        # Validar schema (partial=True permite campos opcionales)
        errors = user_create_schema.validate(data, partial=True)
        if errors:
            print("Errores de validación:", errors)
            return jsonify({"error": "Errores de validación", "details": errors}), 400

        usuario = user_service.update(id, data)
        resultado = user_schema.dump(usuario)
        print("Usuario actualizado exitosamente:", resultado)
        print("=" * 50)
        return jsonify(resultado), 200
        
    except ValueError as e:
        print(f"ValueError: {str(e)}")
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        import traceback
        print("=" * 50)
        print("ERROR AL ACTUALIZAR USUARIO:")
        print(f"Tipo de error: {type(e).__name__}")
        print(f"Mensaje: {str(e)}")
        traceback.print_exc()
        print("=" * 50)
        return jsonify({
            "error": "Error al actualizar el usuario", 
            "details": str(e),
            "type": type(e).__name__
        }), 500

@bp_user.delete('/<int:id>')
@jwt_required()
@role_required(['admin'])
def eliminar_usuario(id):
    try:
        print("=" * 50)
        print(f"ELIMINAR USUARIO - ID: {id}")
        
        user_service.delete(id)
        
        print(f"Usuario {id} eliminado exitosamente")
        print("=" * 50)
        return '', 204 
        
    except ValueError as e:
        print(f"ValueError: {str(e)}")
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        import traceback
        print("=" * 50)
        print("ERROR AL ELIMINAR USUARIO:")
        print(f"Tipo de error: {type(e).__name__}")
        print(f"Mensaje: {str(e)}")
        traceback.print_exc()
        print("=" * 50)
        return jsonify({
            "error": "Error al eliminar el usuario", 
            "details": str(e),
            "type": type(e).__name__
        }), 500