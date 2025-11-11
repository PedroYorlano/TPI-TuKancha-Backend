from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt
from app import db
from app.services.club_service import ClubService
from app.schemas.club_schema import club_schema, clubes_schema
from app.schemas.cancha_schema import canchas_schema
from app.auth.decorators import role_required

bp_club = Blueprint("club", __name__, url_prefix="/api/v1/clubes")

club_service = ClubService(db)

# Listar todos los clubes (PÚBLICO - no requiere autenticación)
@bp_club.get('/')
def listar_clubes():
    clubes = club_service.get_all()
    return jsonify(clubes_schema.dump(clubes))
    
# Obtener un club por su ID (PÚBLICO - no requiere autenticación)
@bp_club.get('/<int:id>')
def obtener_club(id):
    try:
        club = club_service.get_by_id(id)
        if club is None:
            return jsonify({"error": "Club no encontrado"}), 404
        return jsonify(club_schema.dump(club))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Crear un nuevo club (PÚBLICO - para registro de nuevos clubes)
# Si quieres que solo admins puedan crear clubes, agrega @jwt_required() y @role_required(['admin'])
@bp_club.post('/')
def crear_club():
    data = request.get_json()
    try:
        club = club_service.create(data)
        return jsonify(club_schema.dump(club)), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        import traceback
        print("=" * 50)
        print("ERROR AL CREAR CLUB:")
        print(f"Tipo de error: {type(e).__name__}")
        print(f"Mensaje: {str(e)}")
        print("Traceback completo:")
        traceback.print_exc()
        print("=" * 50)
        return jsonify({
            "error": "Error al crear el club",
            "details": str(e),
            "type": type(e).__name__
        }), 500

# Actualizar un club por su ID (PROTEGIDO - solo admin)
@bp_club.put('/<int:id>')
@jwt_required()
@role_required(['admin'])
def actualizar_club(id):
    data = request.get_json()
    try:
        club = club_service.update(id, data)
        return jsonify(club_schema.dump(club)), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": "Error al actualizar el club"}), 500

# Eliminar un club por su ID (PROTEGIDO - solo admin)
@bp_club.delete('/<int:id>')
@jwt_required()
@role_required(['admin'])
def eliminar_club(id):
    try:
        club_service.delete(id)
        return '', 204 
    except ValueError as e:
        return jsonify({"error": "Club no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Listar todas las canchas de un club (PÚBLICO)
@bp_club.get('/<int:id>/canchas')
def listar_canchas_club(id):
    club = club_service.get_by_id(id)
    if club is None:
        return jsonify({"error": "Club no encontrado"}), 404
    canchas = club.canchas
    return jsonify(canchas_schema.dump(canchas))

