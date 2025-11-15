from flask import Blueprint, jsonify, request
from app import db
from app.services.torneos.partido_service import PartidoService
from app.schemas.torneos.partido_schema import partido_schema, partidos_schema

bp_partido = Blueprint("partido", __name__, url_prefix="/api/v1/partidos")

partido_service = PartidoService(db)

# Obtener un partido por su ID
@bp_partido.get('/<int:id>')
def obtener_partido(id):
	partido = partido_service.get_by_id(id)
	return jsonify(partido_schema.dump(partido))

# Crear un nuevo partido
@bp_partido.post('/')
def crear_partido():
	data = request.get_json()
	partido = partido_service.create(data)
	return jsonify({
        "data": partido_schema.dump(partido),
        "message": "Partido creado exitosamente"
    }), 201

# Actualizar un partido por su ID
@bp_partido.put('/<int:id>')
def actualizar_partido(id):
	data = request.get_json()
	partido = partido_service.update(id, data)
	return jsonify({
        "data": partido_schema.dump(partido),
        "message": "Partido actualizado exitosamente"
    }), 200

# Eliminar un partido por su ID
@bp_partido.delete('/<int:id>')
def eliminar_partido(id):
	partido_service.delete(id)
	return jsonify({"message": "Partido eliminado exitosamente"}), 200

# Listar partidos por torneo
@bp_partido.get('/torneo/<int:torneo_id>')
def listar_partidos_torneo(torneo_id):
    partidos = partido_service.get_by_torneo(torneo_id)
    return jsonify(partidos_schema.dump(partidos)), 200

# Registrar resultado de un partido
@bp_partido.patch('/<int:id>/resultado')
def registrar_resultado(id):
    data = request.get_json()
    partido = partido_service.registrar_resultado(id, data)
    return jsonify({
        "data": partido_schema.dump(partido),
        "message": "Resultado registrado exitosamente"
    }), 200


