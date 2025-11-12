from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
from app import db
from app.auth.decorators import role_required
from app.services.equipo_service import EquipoService
from app.schemas.torneos.equipo_schema import equipo_schema, equipos_schema

bp_equipo = Blueprint("equipo", __name__, url_prefix="/api/v1/equipos")
equipo_service = EquipoService(db)

def handle_error(error, status_code=400):
    """Función para manejar errores de manera consistente"""
    return jsonify({"error": str(error)}), status_code

# Obtener todos los equipos
@bp_equipo.get("/")
def get_equipos():
    try:
        equipos = equipo_service.get_all()
        return jsonify({
            "status": "success",
            "data": equipos_schema.dump(equipos)
        }), 200
    except Exception as e:
        return handle_error(f"Error al obtener equipos: {str(e)}", 500)

# Obtener equipo por ID
@bp_equipo.get("/<int:equipo_id>")
def get_equipo(equipo_id):
    try:
        equipo = equipo_service.get_by_id(equipo_id)
        if not equipo:
            return handle_error("Equipo no encontrado", 404)
            
        return jsonify({
            "status": "success",
            "data": equipo_schema.dump(equipo)
        }), 200
    except Exception as e:
        return handle_error(f"Error al obtener el equipo: {str(e)}", 500)

# Obtener equipos por torneo
@bp_equipo.get("/torneo/<int:torneo_id>")
def get_equipos_por_torneo(torneo_id):
    try:
        equipos = equipo_service.get_by_torneo(torneo_id)
        return jsonify({
            "status": "success",
            "data": equipos_schema.dump(equipos)
        }), 200
    except Exception as e:
        return handle_error(f"Error al obtener equipos del torneo: {str(e)}", 500)

# Crear un nuevo equipo
@jwt_required()
@role_required(["ADMIN", "ORGANIZADOR"])
@bp_equipo.post("/")
def create_equipo():
    try:
        equipo_data = request.get_json()
        if not equipo_data:
            return handle_error("No se proporcionaron datos del equipo", 400)
            
        # Validar campos requeridos
        required_fields = ['nombre', 'torneo_id']
        for field in required_fields:
            if field not in equipo_data or not equipo_data[field]:
                return handle_error(f"El campo '{field}' es requerido", 400)
        
        # Crear el equipo
        equipo = equipo_service.create(equipo_data)
        
        return jsonify({
            "status": "success",
            "message": "Equipo creado exitosamente",
            "data": equipo_schema.dump(equipo)
        }), 201
        
    except ValueError as e:
        return handle_error(str(e), 400)
    except Exception as e:
        return handle_error(f"Error al crear el equipo: {str(e)}", 500)

# Actualizar un equipo
@jwt_required()
@role_required(["ADMIN", "ORGANIZADOR"])
@bp_equipo.put("/<int:equipo_id>")
def update_equipo(equipo_id):
    try:
        equipo_data = request.get_json()
        if not equipo_data:
            return handle_error("No se proporcionaron datos para actualizar", 400)
        
        # Actualizar el equipo
        equipo = equipo_service.update(equipo_id, equipo_data)
        
        return jsonify({
            "status": "success",
            "message": "Equipo actualizado exitosamente",
            "data": equipo_schema.dump(equipo)
        }), 200
        
    except ValueError as e:
        return handle_error(str(e), 400)
    except Exception as e:
        return handle_error(f"Error al actualizar el equipo: {str(e)}", 500)

# Eliminar un equipo
@jwt_required()
@role_required(["ADMIN", "ORGANIZADOR"])
@bp_equipo.delete("/<int:equipo_id>")
def delete_equipo(equipo_id):
    try:
        equipo_service.delete(equipo_id)
        
        return jsonify({
            "status": "success",
            "message": "Equipo eliminado exitosamente"
        }), 200
        
    except ValueError as e:
        return handle_error(str(e), 404)
    except Exception as e:
        return handle_error(f"Error al eliminar el equipo: {str(e)}", 500)
