from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services.auth_service import AuthService

bp_auth = Blueprint("auth", __name__, url_prefix="/api/v1/auth")

auth_service = AuthService()


@bp_auth.post('/login')
def login():
    """
    Endpoint de inicio de sesión.
    
    Body (JSON):
        {
            "email": "admin@clubejemplo.com",
            "password": "password123"
        }
    
    Response (200):
        {
            "access_token": "eyJ0eXAiOiJKV1QiLCJ...",
            "refresh_token": "eyJ0eXAiOiJKV1QiLCJ...",
            "user": {
                "id": 1,
                "nombre": "admin",
                "email": "admin@clubejemplo.com",
                "rol": "admin",
                "club_id": 1,
                "club_nombre": "Club Ejemplo"
            }
        }
    """
    data = request.get_json()
    
    # Validar campos requeridos
    if not data or 'email' not in data or 'password' not in data:
        return jsonify({
            "error": "Email y password son requeridos"
        }), 400
    
    try:
        result = auth_service.login(data['email'], data['password'])
        return jsonify(result), 200
    
    except ValueError as e:
        return jsonify({"error": str(e)}), 401
    
    except Exception as e:
        return jsonify({
            "error": "Error al iniciar sesión",
            "details": str(e)
        }), 500


@bp_auth.post('/refresh')
@jwt_required(refresh=True)
def refresh():
    """
    Endpoint para refrescar el access token usando el refresh token.
    
    Headers:
        Authorization: Bearer <refresh_token>
    
    Response (200):
        {
            "access_token": "eyJ0eXAiOiJKV1QiLCJ..."
        }
    """
    try:
        current_user_id = get_jwt_identity()
        result = auth_service.refresh_access_token(current_user_id)
        return jsonify(result), 200
    
    except ValueError as e:
        return jsonify({"error": str(e)}), 401
    
    except Exception as e:
        return jsonify({
            "error": "Error al refrescar token",
            "details": str(e)
        }), 500


@bp_auth.get('/me')
@jwt_required()
def get_current_user():
    """
    Obtiene la información del usuario autenticado actual.
    
    Headers:
        Authorization: Bearer <access_token>
    
    Response (200):
        {
            "id": 1,
            "nombre": "admin",
            "email": "admin@clubejemplo.com",
            "rol": "admin",
            "club_id": 1
        }
    """
    try:
        # Obtener ID del usuario desde el token (viene como string)
        current_user_id_str = get_jwt_identity()
        
        # Obtener claims adicionales del token
        claims = get_jwt()
        
        # Convertir ID a int para retornar
        return jsonify({
            "id": int(current_user_id_str),
            "nombre": claims.get('nombre'),
            "email": claims.get('email'),
            "rol": claims.get('rol'),
            "club_id": claims.get('club_id')
        }), 200
    
    except Exception as e:
        return jsonify({
            "error": "Error al obtener usuario",
            "details": str(e)
        }), 500


@bp_auth.post('/logout')
@jwt_required()
def logout():
    """
    Cierra la sesión del usuario.
    
    Nota: En JWT stateless, el logout se maneja en el frontend
    eliminando el token. Este endpoint existe para compatibilidad
    y podría implementar una blacklist de tokens en el futuro.
    
    Headers:
        Authorization: Bearer <access_token>
    
    Response (200):
        {
            "message": "Sesión cerrada exitosamente"
        }
    """
    # TODO: Implementar blacklist de tokens si es necesario
    # Por ahora, el cliente simplemente elimina el token
    
    return jsonify({
        "message": "Sesión cerrada exitosamente"
    }), 200
