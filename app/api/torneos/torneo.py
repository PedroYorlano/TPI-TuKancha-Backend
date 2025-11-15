from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from app import db
from app.auth.decorators import role_required
from app.services.torneos.torneo_service import TorneoService
from app.services.torneos.equipo_service import EquipoService
from app.schemas.torneos.torneo_schema import torneo_schema, torneos_schema
from app.schemas.torneos.equipo_schema import equipo_schema, equipos_schema
from app.schemas.torneos.tabla_schema import tabla_posiciones_schema

bp_torneo = Blueprint("torneo", __name__, url_prefix="/api/v1/torneos")
torneo_service = TorneoService(db)
equipo_service = EquipoService(db)

# Obtener todos los torneos
@bp_torneo.get("/")
def get_torneos():
    torneos = torneo_service.get_all()
    return jsonify({
            "status": "success",
            "data": torneos_schema.dump(torneos)
        }), 200

# Obtener torneo por id
@bp_torneo.get("/<int:id_torneo>")
def get_torneo_detalle(id_torneo):
    torneo = torneo_service.get_by_id(id_torneo)
    return jsonify({
            "status": "success",
            "data": torneo_schema.dump(torneo)
        }), 200

# Obtener torneos activos
@bp_torneo.get("/activos")
def get_torneos_activos():
    torneos = torneo_service.get_torneos_activos()
    return jsonify({
            "status": "success",
            "data": torneos_schema.dump(torneos)
        }), 200

# Obtener torneos por rango de fechas
@bp_torneo.get("/fecha")
def get_torneos_por_fecha():
    fecha_inicio = request.args.get('fecha_inicio')
    fecha_fin = request.args.get('fecha_fin')
    torneos = torneo_service.get_torneos_por_fecha(fecha_inicio, fecha_fin)
    return jsonify({
            "status": "success",
            "data": torneos_schema.dump(torneos),
            "filtros": {
                "fecha_inicio": fecha_inicio,
                "fecha_fin": fecha_fin
            }
        }), 200

# Obtener equipos de un torneo
@bp_torneo.get("/<int:id_torneo>/equipos")
def obtener_equipos_torneo(id_torneo):
    equipos = equipo_service.get_by_torneo(id_torneo)
    return jsonify({
            "status": "success",
            "data": equipos_schema.dump(equipos)
        }), 200

# Obtener tabla de posiciones de un torneo
@bp_torneo.get("/<int:id_torneo>/posiciones")
def get_tabla_de_posiciones(id_torneo):
    """
    Calcula y devuelve la tabla de posiciones para un torneo específico.
    """
    tabla_data = torneo_service.get_tabla_posiciones(id_torneo)
    
    return jsonify({
            "status": "success",
            "data": tabla_posiciones_schema.dump(tabla_data)
        }), 200

# Crear un nuevo torneo
@jwt_required()
@role_required(["Admin"])
def create_torneo():
    torneo = torneo_service.create(request.get_json())
    return jsonify({
            "status": "success",
            "message": "Torneo creado exitosamente",
            "data": torneo_schema.dump(torneo)
        }), 201

# Actualizar un torneo
@bp_torneo.put("/<int:id_torneo>")
@jwt_required()
@role_required(["Admin"])
def update_torneo(id_torneo):
    torneo = torneo_service.update(id_torneo, request.get_json())
    return jsonify({
            "status": "success",
            "message": "Torneo actualizado exitosamente",
            "data": torneo_schema.dump(torneo)
        }), 200

# Cambiar estado de un torneo
@bp_torneo.put("/<int:id_torneo>/estado")
@jwt_required()
@role_required(["Admin"])
def cambiar_estado_torneo(id_torneo):
    data = request.get_json()
    torneo = torneo_service.cambiar_estado(id_torneo, data)
            
    return jsonify({
            "status": "success",
            "message": f"Estado del torneo cambiado exitosamente",
            "data": torneo_schema.dump(torneo)
        }), 200

# Agregar equipo a un torneo
@bp_torneo.put("/<int:id_torneo>/equipo")
@jwt_required()
@role_required(["Admin"])
def agregar_equipo_torneo(id_torneo):
    torneo = torneo_service.agregar_equipo(id_torneo, request.get_json())
    return jsonify({
            "status": "success",
            "message": "Equipo agregado al torneo exitosamente",
            "data": torneo_schema.dump(torneo)
        }), 200

# Eliminar un torneo
@bp_torneo.delete("/<int:id_torneo>")
@jwt_required()
@role_required(["Admin"])
def delete_torneo(id_torneo):
    torneo_service.delete(id_torneo)
    return jsonify({
            "status": "success",
            "message": "Torneo eliminado exitosamente"
        }), 200
