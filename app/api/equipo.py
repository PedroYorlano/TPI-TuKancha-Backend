from flask import Blueprint, jsonify, request
from app import db
from app.services.equipo_service import EquipoService
from app.schemas.equipo_schema import equipo_schema, equipos_schema

bp_equipo = Blueprint("equipo", __name__, url_prefix="/api/v1/equipos")

equipo_service = EquipoService(db)


# Listar todos los equipos
@bp_equipo.get('/')
def listar_equipos():
    equipos = equipo_service.get_all()
    return jsonify(equipos_schema.dump(equipos))
    
# Obtener un equipo por su ID
@bp_equipo.get('/<int:id>')
def obtener_equipo(id):
    try:
        equipo = equipo_service.get_by_id(id)
        if equipo is None:
            return jsonify({"error": "Equipo no encontrado"}), 404
        return jsonify(equipo_schema.dump(equipo))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Crear un nuevo equipo
@bp_equipo.post('/')
def crear_equipo():
    data = request.get_json()
    try:
        equipo = equipo_service.create(data)
        return jsonify(equipo_schema.dump(equipo)), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Error al crear el equipo"}), 500

# Actualizar un equipo por su ID
@bp_equipo.put('/<int:id>')
def actualizar_equipo(id):
    data = request.get_json()
    try:
        equipo = equipo_service.update(id, data)
        return jsonify(equipo_schema.dump(equipo)), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": "Error al actualizar el equipo"}), 500

# Eliminar un equipo por su ID
@bp_equipo.delete('/<int:id>')
def eliminar_equipo(id):
    try:
        equipo_service.delete(id)
        return '', 204 
    except ValueError as e:
        return jsonify({"error": "Equipo no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Listar equipos por torneo
@bp_equipo.get('/torneo/<int:torneo_id>')
def listar_equipos_torneo(torneo_id):
    try:
        equipos = equipo_service.get_by_torneo(torneo_id)
        return jsonify(equipos_schema.dump(equipos))
    except Exception as e:
        return jsonify({"error": str(e)}), 500
