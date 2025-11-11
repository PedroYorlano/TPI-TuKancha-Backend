from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from app import db
from app.auth.decorators import role_required
from app.services.cancha_service import CanchaService
from app.schemas.cancha_schema import cancha_schema, canchas_schema
from app.schemas.timeslot_schema import timeslots_schema

bp_cancha = Blueprint("cancha", __name__, url_prefix="/api/v1/canchas")
cancha_service = CanchaService(db)

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

# Crear una nueva cancha
@bp_cancha.post("/")
@jwt_required()
@role_required(['admin'])
def create_cancha():
    data = request.get_json()
    try:
        cancha = cancha_service.create(data)
        return jsonify(cancha_schema.dump(cancha)), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Error al crear la cancha"}), 500

# Actualizar una cancha
@bp_cancha.put("/<int:id_cancha>")
def update_cancha(id_cancha):
    data = request.get_json()
    try:
        cancha = cancha_service.update(id_cancha, data)
        return jsonify(cancha_schema.dump(cancha)), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": "Error al actualizar la cancha"}), 500

# Eliminar una cancha
@bp_cancha.delete("/<int:id_cancha>")
def delete_cancha(id_cancha):
    try:
        cancha = cancha_service.get_by_id(id_cancha)
        if not cancha:
            return jsonify({"error": "Cancha no encontrada"}), 404
        cancha_service.delete(id_cancha)
        return '', 204 
    except ValueError as e:
        return jsonify({"error": "Cancha no encontrada"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Obtener los timeslots de una cancha
@bp_cancha.get("/<int:id_cancha>/timeslots")
def get_timeslots_cancha(id_cancha):
    try:
        cancha = cancha_service.get_by_id(id_cancha)
        if not cancha:
            return jsonify({"error": "Cancha no encontrada"}), 404
        timeslots = cancha.timeslots
        return jsonify(timeslots_schema.dump(timeslots)), 200
    except ValueError as e:
        return jsonify({"error": "Cancha no encontrada"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500