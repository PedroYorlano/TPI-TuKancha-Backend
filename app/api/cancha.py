from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from app import db
from app.auth.decorators import role_required
from app.services.cancha_service import CanchaService
from app.schemas.cancha_schema import cancha_schema, canchas_schema
from app.schemas.timeslot_schema import timeslots_schema

bp_cancha = Blueprint("cancha", __name__, url_prefix="/api/v1/canchas")
cancha_service = CanchaService(db)

from app.errors import NotFoundError, ValidationError, AppError, ConflictError

# Obtener todas las canchas
@bp_cancha.get("/")
def get_canchas():
    canchas = cancha_service.get_all()
    return jsonify(canchas_schema.dump(canchas))

# Obtener cancha por id
@bp_cancha.get("/<int:id_cancha>")
def get_cancha_detalle(id_cancha):
    cancha = cancha_service.get_by_id(id_cancha)
    return jsonify(cancha_schema.dump(cancha))

# Obtener todas las canchas de un club específico
@bp_cancha.get("/club/<int:club_id>")
@jwt_required()
def get_canchas_by_club(club_id):
    canchas = cancha_service.get_by_club(club_id)
    return jsonify(canchas_schema.dump(canchas)), 200
    
# Crear una nueva cancha
@bp_cancha.post("/")
@jwt_required()
@role_required(['admin'])
def create_cancha():
    data = request.get_json()
    cancha = cancha_service.create(data)
    return jsonify(cancha_schema.dump(cancha)), 201

# Actualizar una cancha
@bp_cancha.put("/<int:id_cancha>")
@jwt_required()
@role_required(['admin', 'encargado'])
def update_cancha(id_cancha):
    data = request.get_json()
    cancha = cancha_service.update(id_cancha, data)
    return jsonify(cancha_schema.dump(cancha)), 200

# Eliminar una cancha
@bp_cancha.delete("/<int:id_cancha>")
@jwt_required()
@role_required(['admin'])
def delete_cancha(id_cancha):
    cancha_service.delete(id_cancha)
    return jsonify({"message": "Cancha eliminada exitosamente"}), 200 

# Obtener los timeslots de una cancha
@bp_cancha.get("/<int:id_cancha>/timeslots")
def get_timeslots_cancha(id_cancha):
    cancha = cancha_service.get_by_id(id_cancha)
    timeslots = cancha.timeslots
    return jsonify(timeslots_schema.dump(timeslots)), 200