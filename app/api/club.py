from flask import Blueprint, jsonify, request
from app import db
from app.services.club_service import ClubService

bp = Blueprint("club", __name__, url_prefix="/api/v1/club")

club_service = ClubService(db)

# Listar todos los clubes
@bp.get('/')
def listar_clubes():
    clubes = club_service.get_all()
    return jsonify([{"id": c.id, "nombre": c.nombre} for c in clubes])
    
# Obtener un club por su ID
@bp.get('/<int:id>')
def obtener_club(id):
    try:
        club = club_service.get_by_id(id)
        if club is None:
            return jsonify({"error": "Club no encontrado"}), 404
        return jsonify({"id": club.id, "nombre": club.nombre})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Crear un nuevo club
@bp.post('/')
def crear_club():
    data = request.get_json()
    try:
        club = club_service.create(data)
        return jsonify({
            "id": club.id,
            "nombre": club.nombre,
            "cuit": club.cuit,
            "telefono": club.telefono,
            "direccion_id": club.direccion_id
        }), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Error al crear el club"}), 500

# Actualizar un club por su ID
@bp.put('/<int:id>')
def actualizar_club(id):
    data = request.get_json()
    try:
        club = club_service.update(id, data)
        return jsonify({
            "id": club.id,
            "nombre": club.nombre,
            "cuit": club.cuit,
            "telefono": club.telefono,
            "direccion_id": club.direccion_id,
            "message": "Club actualizado correctamente"
        }), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": "Error al actualizar el club"}), 500

# Eliminar un club por su ID
@bp.delete('/<int:id>')
def eliminar_club(id):
    try:
        club = club_service.get_by_id(id)
        if club is None:
            return jsonify({"error": "Club no encontrado"}), 404
        club_service.delete(id)
        return jsonify({"message": "Club eliminado"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
