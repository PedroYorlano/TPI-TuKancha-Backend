from flask import Blueprint, jsonify, request
from app import db
from app.services.club_service import ClubService
from app.schemas.club_schema import club_schema, clubes_schema
from app.schemas.cancha_schema import canchas_schema

bp_club = Blueprint("club", __name__, url_prefix="/api/v1/clubes")

club_service = ClubService(db)

# Listar todos los clubes
@bp_club.get('/')
def listar_clubes():
    clubes = club_service.get_all()
    return jsonify(clubes_schema.dump(clubes))
    
# Obtener un club por su ID
@bp_club.get('/<int:id>')
def obtener_club(id):
    try:
        club = club_service.get_by_id(id)
        if club is None:
            return jsonify({"error": "Club no encontrado"}), 404
        return jsonify(club_schema.dump(club))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Crear un nuevo club
@bp_club.post('/')
def crear_club():
    data = request.get_json()
    try:
        club = club_service.create(data)
        return jsonify(club_schema.dump(club)), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Error al crear el club"}), 500

# Actualizar un club por su ID
@bp_club.put('/<int:id>')
def actualizar_club(id):
    data = request.get_json()
    try:
        club = club_service.update(id, data)
        return jsonify(club_schema.dump(club)), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": "Error al actualizar el club"}), 500

# Eliminar un club por su ID
@bp_club.delete('/<int:id>')
def eliminar_club(id):
    try:
        club_service.delete(id)
        return '', 204 
    except ValueError as e:
        return jsonify({"error": "Club no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Listar todas las canchas de un club
@bp_club.get('/<int:id>/canchas')
def listar_canchas_club(id):
    club = club_service.get_by_id(id)
    if club is None:
        return jsonify({"error": "Club no encontrado"}), 404
    canchas = club.canchas
    return jsonify(canchas_schema.dump(canchas))

