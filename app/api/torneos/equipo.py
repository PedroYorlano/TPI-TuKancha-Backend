from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
from app import db
from app.auth.decorators import role_required
from app.services.torneos.equipo_service import EquipoService
from app.schemas.torneos.equipo_schema import equipo_schema, equipos_schema

bp_equipo = Blueprint("equipo", __name__, url_prefix="/api/v1/equipos")
equipo_service = EquipoService(db)

def handle_error(error, status_code=400):
    """Función para manejar errores de manera consistente"""
    return jsonify({"error": str(error)}), status_code

# Obtener todos los equipos
@bp_equipo.get("/")
def get_equipos():
    equipos = equipo_service.get_all()
    return jsonify(equipos_schema.dump(equipos)), 200

# Obtener equipo por ID
@bp_equipo.get("/<int:equipo_id>")
def get_equipo(equipo_id):
    equipo = equipo_service.get_by_id(equipo_id)
    return jsonify(equipo_schema.dump(equipo)), 200

# Crear un nuevo equipo
@jwt_required()
@role_required(["Admin"])
@bp_equipo.post("/")
def create_equipo():
    equipo_data = request.get_json()
    equipo = equipo_service.create(equipo_data)
    return jsonify({
        "message": "Equipo creado exitosamente",
        "data": equipo_schema.dump(equipo)
    }), 201

# Actualizar un equipo
@jwt_required()
@role_required(["Admin"])
@bp_equipo.put("/<int:equipo_id>")
def update_equipo(equipo_id):
    equipo_data = request.get_json()
    equipo = equipo_service.update(equipo_id, equipo_data)
    return jsonify({
        "message": "Equipo actualizado exitosamente",
        "data": equipo_schema.dump(equipo)
    }), 200

# Eliminar un equipo
@jwt_required()
@role_required(["Admin"])
@bp_equipo.delete("/<int:equipo_id>")
def delete_equipo(equipo_id):
    equipo_service.delete(equipo_id)
    return jsonify({
        "message": "Equipo eliminado exitosamente"
    }), 200
