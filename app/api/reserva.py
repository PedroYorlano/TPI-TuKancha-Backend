from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from app import db
from app.services.reserva_service import ReservaService
from app.schemas.reserva_schema import reserva_schema, reservas_schema
from app.auth.decorators import role_required

bp_reserva = Blueprint("reserva", __name__, url_prefix="/api/v1/reservas")

reserva_service = ReservaService()

# Obtener todas las reservas
@bp_reserva.get("/")
@jwt_required()
@role_required(['admin', 'encargado'])
def get_all():
    reservas = reserva_service.get_all()
    return reservas_schema.dump(reservas)

# Obtener reservas por club ID
@bp_reserva.get("/club/<int:club_id>")
@jwt_required()
@role_required(['admin', 'encargado'])
def get_by_club(club_id):
    """
    Obtiene todas las reservas de un club específico.
    
    Requiere autenticación JWT y rol de 'admin' o 'encargado'.
    
    Response (200):
        Lista de reservas del club
    """
    reservas = reserva_service.get_by_club_id(club_id)
    return jsonify(reservas_schema.dump(reservas)), 200

# Obtener una reserva por su ID
@bp_reserva.get("/<int:id>")
@jwt_required()
@role_required(['admin', 'encargado'])
def get_by_id(id):
    reserva = reserva_service.get_by_id(id)
    return reserva_schema.dump(reserva)


# Crear una nueva reserva
@bp_reserva.post("/")
def create():
    data = request.json
    reserva = reserva_service.create(data)
    return jsonify(reserva_schema.dump(reserva)), 201

# Marcar una reserva como pagada
@bp_reserva.put("/<int:id>/pagar")
@jwt_required()
@role_required(['admin', 'encargado'])
def marcar_pagada(id):
    reserva_service.marcar_reserva_pagada(id)
    return jsonify({"message": "Reserva marcada como pagada exitosamente"}), 200

# Cancelar una reserva
@bp_reserva.delete("/<int:id>")
@jwt_required()
@role_required(['admin', 'encargado'])
def delete(id):
    reserva_service.cancelar_reserva(id) # Usar el método seguro para cancelar reserva
    return jsonify({"message": "Reserva cancelada exitosamente"}), 200



