from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
from datetime import datetime
from app import db
from app.auth.decorators import role_required
from app.services.torneos.torneo_service import TorneoService
from app.services.torneos.equipo_service import EquipoService
from app.schemas.torneos.torneo_schema import torneo_schema, torneos_schema
from app.schemas.torneos.equipo_schema import equipo_schema, equipos_schema
from app.models.enums import TorneoEstado
import logging

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

# Crear un nuevo torneo
@jwt_required()
@role_required(["Admin"])
@bp_torneo.post("/")
def create_torneo():
    torneo_data = request.get_json()
    required_fields = ['nombre', 'club_id', 'fecha_inicio']
    
    # Crear el torneo
    torneo = torneo_service.create(torneo_data)
    
    return jsonify({
            "status": "success",
            "message": "Torneo creado exitosamente",
            "data": torneo_schema.dump(torneo)
        }), 201

# Actualizar un torneo
@jwt_required()
@role_required(["Admin"])
@bp_torneo.put("/<int:id_torneo>")
def update_torneo(id_torneo):
    torneo_data = request.get_json()
        
    # Actualizar el torneo
    torneo = torneo_service.update(id_torneo, torneo_data)
        
    if not torneo:
        return jsonify({"error": "Torneo no encontrado"}), 404
            
    return jsonify({
            "status": "success",
            "message": "Torneo actualizado exitosamente",
            "data": torneo_schema.dump(torneo)
        }), 200

# Eliminar un torneo
@jwt_required()
@role_required(["Admin"])
@bp_torneo.delete("/<int:id_torneo>")
def delete_torneo(id_torneo):
    torneo = torneo_service.get_by_id(id_torneo)
         
    # Eliminar el torneo
    torneo_service.delete(id_torneo)
        
    return jsonify({
            "status": "success",
            "message": "Torneo eliminado exitosamente"
        }), 200

# Cambiar estado de un torneo
@jwt_required()
@role_required(["Admin"])
@bp_torneo.put("/<int:id_torneo>/estado")
def cambiar_estado_torneo(id_torneo):
    data = request.get_json()
    if not data or 'estado' not in data:
        return jsonify({"error": "El campo 'estado' es requerido"}), 400
            
    estado = data['estado']
   
    # Cambiar el estado del torneo
    torneo = torneo_service.cambiar_estado(id_torneo, estado)
            
    return jsonify({
            "status": "success",
            "message": f"Estado del torneo cambiado a '{estado}' exitosamente",
            "data": torneo_schema.dump(torneo)
        }), 200

# Agregar un equipo al torneo
@jwt_required()
@role_required(["Admin"])
@bp_torneo.put("/<int:id_torneo>/equipo")
def agregar_equipo_torneo(id_torneo):
    equipo_data = request.get_json()    
    # Agregar el equipo al torneo
    torneo = torneo_service.agregar_equipo(id_torneo, equipo_data)
            
    return jsonify({
            "status": "success",
            "message": "Equipo agregado al torneo exitosamente",
            "data": torneo_schema.dump(torneo)
        }), 200

# Obtener los equipos de un torneo
@bp_torneo.get("/<int:id_torneo>/equipos")
def obtener_equipos_torneo(id_torneo):
    equipos = equipo_service.get_by_torneo(id_torneo)
    return jsonify({
            "status": "success",
            "data": equipos_schema.dump(equipos)
        }), 200




