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
    usuarios = user_service.get_all()
    return jsonify(users_schema.dump(usuarios)), 200

@bp_user.get('/<int:id>')
@jwt_required()
@role_required(['admin'])
def obtener_usuario(id):
    usuario = user_service.get_by_id(id)
    return jsonify(user_schema.dump(usuario)), 200

@bp_user.get('/club/<int:club_id>')
@jwt_required()
@role_required(['admin'])
def obtener_usuarios_por_club(club_id):
    usuarios = user_service.get_by_club(club_id)
    return jsonify(users_schema.dump(usuarios)), 200

@bp_user.get('/check-email/<email>')
def verificar_email(email):
    """Endpoint público para verificar si un email ya está registrado"""
    existe = user_service.email_exists(email)
    return jsonify({
        "email": email,
        "registrado": existe
    }), 200

@bp_user.post('/')
@jwt_required()
@role_required(['admin'])
def crear_usuario():
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No se recibió ningún dato JSON"}), 400
        
    print("=" * 50)
    print("CREAR USUARIO - Datos recibidos:", data)

    # El servicio crea el usuario (con el hashing)
    nuevo_usuario = user_service.create(data)
    
    # Se devuelve la SALIDA formateada con 'user_schema' (sin password)
    resultado = user_schema.dump(nuevo_usuario)
    print("Usuario creado exitosamente:", resultado)
    print("=" * 50)
    return jsonify(resultado), 201

@bp_user.patch('/<int:id>')
@jwt_required()
@role_required(['admin'])
def actualizar_usuario(id):
    data = request.get_json()
    usuario = user_service.update(id, data)
    resultado = user_schema.dump(usuario)
    print("Usuario actualizado exitosamente:", resultado)
    print("=" * 50)
    return jsonify(resultado), 200

@bp_user.delete('/<int:id>')
@jwt_required()
@role_required(['admin'])
def eliminar_usuario(id):
    user_service.delete(id)
    return jsonify({"message": "Usuario eliminado exitosamente"}), 200 