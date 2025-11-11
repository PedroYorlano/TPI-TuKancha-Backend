from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt, verify_jwt_in_request


def role_required(allowed_roles):
    """
    Decorador para proteger rutas por rol.
    
    Uso:
        @bp.route('/admin-only')
        @jwt_required()
        @role_required(['admin'])
        def admin_route():
            return "Solo admins pueden acceder"
    
    Args:
        allowed_roles (list): Lista de roles permitidos ['admin', 'encargado']
    
    Returns:
        Decorador que verifica si el usuario tiene uno de los roles permitidos
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            # Verificar que el JWT sea válido
            verify_jwt_in_request()
            
            # Obtener los claims del JWT
            claims = get_jwt()
            user_role = claims.get('rol')
            
            # Verificar si el rol del usuario está en la lista de roles permitidos
            if user_role not in allowed_roles:
                return jsonify({
                    "error": "Acceso denegado",
                    "message": f"Se requiere uno de estos roles: {', '.join(allowed_roles)}"
                }), 403
            
            # Si tiene el rol correcto, ejecutar la función
            return fn(*args, **kwargs)
        
        return wrapper
    return decorator


def club_access_required(fn):
    """
    Decorador para verificar que el usuario solo acceda a datos de su club.
    
    Uso:
        @bp.route('/club/<int:club_id>')
        @jwt_required()
        @club_access_required
        def get_club_data(club_id):
            # Solo puede acceder si club_id coincide con su club
            return "Datos del club"
    
    El decorador verifica:
    - Admins pueden acceder a cualquier club
    - Otros roles solo pueden acceder a su propio club
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        
        claims = get_jwt()
        user_role = claims.get('rol')
        user_club_id = claims.get('club_id')
        
        # Si es admin, puede acceder a cualquier club
        if user_role == 'admin':
            return fn(*args, **kwargs)
        
        # Para otros roles, verificar que el club_id coincida
        # Buscar club_id en kwargs (parámetros de ruta) o args
        requested_club_id = kwargs.get('club_id') or kwargs.get('id')
        
        if requested_club_id and requested_club_id != user_club_id:
            return jsonify({
                "error": "Acceso denegado",
                "message": "Solo puedes acceder a datos de tu club"
            }), 403
        
        return fn(*args, **kwargs)
    
    return wrapper
