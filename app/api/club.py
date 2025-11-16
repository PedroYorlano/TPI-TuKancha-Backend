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
    club = club_service.get_by_id(id)
    return jsonify(club_schema.dump(club))

# Crear un nuevo club (PÚBLICO - para registro de nuevos clubes)
@bp_club.post('/')
def crear_club():
    data = request.get_json()
    club = club_service.create(data)
    return jsonify(club_schema.dump(club)), 201

# Actualizar un club por su ID (PROTEGIDO - solo admin)
@bp_club.put('/<int:id>')
@jwt_required()
@role_required(['admin'])
def actualizar_club(id):
    data = request.get_json()
    club = club_service.update(id, data)
    return jsonify(club_schema.dump(club)), 200

# Eliminar un club por su ID (PROTEGIDO - solo admin)
@bp_club.delete('/<int:id>')
@jwt_required()
@role_required(['admin'])
def eliminar_club(id):
    club_service.delete(id)
    return jsonify({"message": "Club eliminado exitosamente"}), 200 

# Listar todas las canchas de un club (PÚBLICO)
@bp_club.get('/<int:id>/canchas')
def listar_canchas_club(id):
    club = club_service.get_by_id(id)
    canchas = club.canchas
    return jsonify(canchas_schema.dump(canchas))

