from flask import Blueprint, jsonify, request
from app import db
from app.services.reserva_service import ReservaService
from app.schemas.reserva_schema import reserva_schema, reservas_schema

bp_reserva = Blueprint("reserva", __name__, url_prefix="/api/v1/reservas")

reserva_service = ReservaService()

# Obtener todas las reservas
@bp_reserva.get("/")
def get_all():
    reservas = reserva_service.get_all()
    return reservas_schema.dump(reservas)

# Obtener una reserva por su ID
@bp_reserva.get("/<int:id>")
def get_by_id(id):
    reserva = reserva_service.get_by_id(id)
    return reserva_schema.dump(reserva)

# Crear una nueva reserva
@bp_reserva.post("/")
def create():
    data = request.json
    reserva = reserva_service.create(data)
    return reserva_schema.dump(reserva)

