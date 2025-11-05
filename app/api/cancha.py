from flask import Blueprint, jsonify, request
from app import db
from app.services.cancha_service import CanchaService

bp_canchas = Blueprint("cancha", __name__, url_prefix="/api/v1/canchas")

@bp_canchas.get("/<int:id_cancha>")
def get_cancha_detalle(id_cancha):
    cancha = CanchaService.get_by_id(id_cancha)
    return jsonify({"id": cancha.id, "nombre": cancha.nombre})

@bp_canchas.put("/<int:id_cancha>")
def update_cancha(id_cancha):
    cancha = CanchaService.get_by_id(id_cancha)
    return jsonify({"id": cancha.id, "nombre": cancha.nombre})

@bp_canchas.delete("/<int:id_cancha>")
def delete_cancha(id_cancha):
    cancha = CanchaService.get_by_id(id_cancha)
    return jsonify({"id": cancha.id, "nombre": cancha.nombre})