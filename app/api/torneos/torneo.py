from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
from datetime import datetime
from app import db
from app.auth.decorators import role_required
from app.services.torneos.torneo_service import TorneoService
from app.schemas.torneos.torneo_schema import torneo_schema, torneos_schema
from app.models.enums import TorneoEstado

# Esquema para validar fechas en formato DD-MM-YYYY
def validate_date_format(date_str):
    try:
        return datetime.strptime(date_str, '%d-%m-%Y').date()
    except ValueError:
        raise ValidationError("Formato de fecha inválido. Use DD-MM-YYYY")

# Función para manejar errores comunes
def handle_error(error, status_code=400):
    return jsonify({"error": str(error)}), status_code

bp_torneo = Blueprint("torneo", __name__, url_prefix="/api/v1/torneos")
torneo_service = TorneoService(db)

# Obtener todos los torneos
@bp_torneo.get("/")
def get_torneos():
    try:
        torneos = torneo_service.get_all()
        return jsonify({
            "status": "success",
            "data": torneos_schema.dump(torneos)
        }), 200
    except Exception as e:
        return handle_error(f"Error al obtener torneos: {str(e)}", 500)

# Obtener torneo por id
@bp_torneo.get("/<int:id_torneo>")
def get_torneo_detalle(id_torneo):
    try:
        torneo = torneo_service.get_by_id(id_torneo)
        if not torneo:
            return handle_error("Torneo no encontrado", 404)
            
        return jsonify({
            "status": "success",
            "data": torneo_schema.dump(torneo)
        }), 200
    except Exception as e:
        return handle_error(f"Error al obtener el torneo: {str(e)}", 500)

# Obtener torneos activos
@bp_torneo.get("/activos")
def get_torneos_activos():
    try:
        torneos = torneo_service.get_torneos_activos()
        return jsonify({
            "status": "success",
            "data": torneos_schema.dump(torneos)
        }), 200
    except Exception as e:
        return handle_error(f"Error al obtener torneos activos: {str(e)}", 500)

# Obtener torneos por rango de fechas
@bp_torneo.get("/fecha")
def get_torneos_por_fecha():
    try:
        fecha_inicio = request.args.get('fecha_inicio')
        fecha_fin = request.args.get('fecha_fin')
        
        if not fecha_inicio:
            return handle_error("El parámetro 'fecha_inicio' es requerido", 400)
            
        # Validar formato de fechas
        try:
            fecha_inicio_dt = validate_date_format(fecha_inicio)
            fecha_fin_dt = validate_date_format(fecha_fin) if fecha_fin else None
        except ValidationError as e:
            return handle_error(str(e), 400)
            
        torneos = torneo_service.get_torneos_por_fecha(fecha_inicio_dt, fecha_fin_dt)
        
        return jsonify({
            "status": "success",
            "data": torneos_schema.dump(torneos),
            "filtros": {
                "fecha_inicio": fecha_inicio,
                "fecha_fin": fecha_fin
            }
        }), 200
    except Exception as e:
        return handle_error(f"Error al buscar torneos por fecha: {str(e)}", 500)

# Crear un nuevo torneo
@jwt_required()
@role_required(["ADMIN", "ORGANIZADOR"])
@bp_torneo.post("/")
def create_torneo():
    try:
        torneo_data = request.get_json()
        if not torneo_data:
            return handle_error("No se proporcionaron datos del torneo", 400)
            
        # Validar campos requeridos
        required_fields = ['nombre', 'club_id', 'fecha_inicio']
        for field in required_fields:
            if field not in torneo_data or not torneo_data[field]:
                return handle_error(f"El campo '{field}' es requerido", 400)
                
        # Validar fechas
        try:
            if 'fecha_inicio' in torneo_data:
                torneo_data['fecha_inicio'] = validate_date_format(torneo_data['fecha_inicio'])
            if 'fecha_fin' in torneo_data and torneo_data['fecha_fin']:
                torneo_data['fecha_fin'] = validate_date_format(torneo_data['fecha_fin'])
        except ValidationError as e:
            return handle_error(str(e), 400)
            
        # Validar estado si se proporciona
        if 'estado' in torneo_data:
            if torneo_data['estado'] not in [e.value for e in TorneoEstado]:
                return handle_error(
                    f"Estado inválido. Debe ser uno de: {', '.join([e.value for e in TorneoEstado])}", 
                    400
                )
        
        # Obtener el ID del usuario autenticado
        current_user_id = get_jwt_identity()
        torneo_data['creado_por'] = current_user_id
        
        # Crear el torneo
        torneo = torneo_service.create(torneo_data)
        
        return jsonify({
            "status": "success",
            "message": "Torneo creado exitosamente",
            "data": torneo_schema.dump(torneo)
        }), 201
        
    except ValidationError as e:
        return handle_error(f"Error de validación: {str(e)}", 400)
    except ValueError as e:
        return handle_error(str(e), 400)
    except Exception as e:
        db.session.rollback()
        return handle_error(f"Error al crear el torneo: {str(e)}", 500)

# Actualizar un torneo
@jwt_required()
@role_required(["ADMIN", "ORGANIZADOR"])
@bp_torneo.put("/<int:id_torneo>")
def update_torneo(id_torneo):
    try:
        torneo_data = request.get_json()
        if not torneo_data:
            return handle_error("No se proporcionaron datos para actualizar", 400)
            
        # Validar fechas si se proporcionan
        if 'fecha_inicio' in torneo_data:
            try:
                torneo_data['fecha_inicio'] = validate_date_format(torneo_data['fecha_inicio'])
            except ValidationError as e:
                return handle_error(f"Formato de fecha_inicio inválido: {str(e)}", 400)
                
        if 'fecha_fin' in torneo_data and torneo_data['fecha_fin']:
            try:
                torneo_data['fecha_fin'] = validate_date_format(torneo_data['fecha_fin'])
            except ValidationError as e:
                return handle_error(f"Formato de fecha_fin inválido: {str(e)}", 400)
        
        # Validar estado si se proporciona
        if 'estado' in torneo_data:
            if torneo_data['estado'] not in [e.value for e in TorneoEstado]:
                return handle_error(
                    f"Estado inválido. Debe ser uno de: {', '.join([e.value for e in TorneoEstado])}", 
                    400
                )
        
        # Actualizar el torneo
        torneo = torneo_service.update(id_torneo, torneo_data)
        
        if not torneo:
            return handle_error("Torneo no encontrado", 404)
            
        return jsonify({
            "status": "success",
            "message": "Torneo actualizado exitosamente",
            "data": torneo_schema.dump(torneo)
        }), 200
        
    except ValidationError as e:
        return handle_error(f"Error de validación: {str(e)}", 400)
    except ValueError as e:
        return handle_error(str(e), 400)
    except Exception as e:
        db.session.rollback()
        return handle_error(f"Error al actualizar el torneo: {str(e)}", 500)

# Eliminar un torneo
@jwt_required()
@role_required(["ADMIN", "ORGANIZADOR"])
@bp_torneo.delete("/<int:id_torneo>")
def delete_torneo(id_torneo):
    try:
        # Verificar si el torneo existe
        torneo = torneo_service.get_by_id(id_torneo)
        if not torneo:
            return handle_error("Torneo no encontrado", 404)
            
        # Eliminar el torneo
        torneo_service.delete(id_torneo)
        
        return jsonify({
            "status": "success",
            "message": "Torneo eliminado exitosamente"
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return handle_error(f"Error al eliminar el torneo: {str(e)}", 500)

# Cambiar estado de un torneo
@jwt_required()
@role_required(["ADMIN", "ORGANIZADOR"])
@bp_torneo.put("/<int:id_torneo>/estado")
def cambiar_estado_torneo(id_torneo):
    try:
        data = request.get_json()
        if not data or 'estado' not in data:
            return handle_error("El campo 'estado' es requerido", 400)
            
        estado = data['estado']
        
        # Validar que el estado sea válido
        if estado not in [e.value for e in TorneoEstado]:
            return handle_error(
                f"Estado inválido. Debe ser uno de: {', '.join([e.value for e in TorneoEstado])}", 
                400
            )
        
        # Cambiar el estado del torneo
        torneo = torneo_service.cambiar_estado(id_torneo, estado)
        
        if not torneo:
            return handle_error("Torneo no encontrado", 404)
            
        return jsonify({
            "status": "success",
            "message": f"Estado del torneo cambiado a '{estado}' exitosamente",
            "data": torneo_schema.dump(torneo)
        }), 200
        
    except ValueError as e:
        return handle_error(str(e), 400)
    except Exception as e:
        db.session.rollback()
        return handle_error(f"Error al cambiar el estado del torneo: {str(e)}", 500)

# Agregar un equipo al torneo
@jwt_required()
@role_required(["ADMIN", "ORGANIZADOR"])
@bp_torneo.put("/<int:id_torneo>/equipo")
def agregar_equipo_torneo(id_torneo):
    try:
        equipo_data = request.get_json()
        if not equipo_data:
            return handle_error("No se proporcionaron datos del equipo", 400)
            
        # Validar campos requeridos
        required_fields = ['equipo_id']
        for field in required_fields:
            if field not in equipo_data or not equipo_data[field]:
                return handle_error(f"El campo '{field}' es requerido", 400)
        
        # Agregar el equipo al torneo
        torneo = torneo_service.agregar_equipo(id_torneo, equipo_data)
        
        if not torneo:
            return handle_error("Torneo no encontrado", 404)
            
        return jsonify({
            "status": "success",
            "message": "Equipo agregado al torneo exitosamente",
            "data": torneo_schema.dump(torneo)
        }), 200
        
    except ValueError as e:
        return handle_error(str(e), 400)
    except Exception as e:
        db.session.rollback()
        return handle_error(f"Error al agregar el equipo al torneo: {str(e)}", 500)



