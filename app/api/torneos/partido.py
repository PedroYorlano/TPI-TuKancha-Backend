from flask import Blueprint, jsonify, request
from app import db
from app.services.torneos.partido_service import PartidoService
from app.schemas.torneos.partido_schema import partido_schema, partidos_schema

bp_partido = Blueprint("partido", __name__, url_prefix="/api/v1/partidos")

partido_service = PartidoService(db)

# Obtener un partido por su ID
@bp_partido.get('/<int:id>')
def obtener_partido(id):
	try:
		partido = partido_service.get_by_id(id)
		if partido is None:
			return jsonify({"error": "Partido no encontrado"}), 404
		return jsonify(partido_schema.dump(partido))
	except Exception as e:
		return jsonify({"error": str(e)}), 500

# Crear un nuevo partido
@bp_partido.post('/')
def crear_partido():
	data = request.get_json()
	try:
		partido = partido_service.create(data)
		return jsonify(partido_schema.dump(partido)), 201
	except ValueError as e:
		return jsonify({"error": str(e)}), 400
	except Exception as e:
		return jsonify({"error": "Error al crear el partido" + str(e)}), 500

# Actualizar un partido por su ID
@bp_partido.put('/<int:id>')
def actualizar_partido(id):
	data = request.get_json()
	try:
		partido = partido_service.update(id, data)
		return jsonify(partido_schema.dump(partido)), 200
	except ValueError as e:
		return jsonify({"error": str(e)}), 404
	except Exception as e:
		return jsonify({"error": "Error al actualizar el partido"}), 500

# Eliminar un partido por su ID
@bp_partido.delete('/<int:id>')
def eliminar_partido(id):
	try:
		partido_service.delete(id)
		return '', 204 
	except ValueError as e:
		return jsonify({"error": "Partido no encontrado"}), 404
	except Exception as e:
		return jsonify({"error": str(e)}), 500

# Listar partidos por torneo
@bp_partido.get('/torneo/<int:torneo_id>')
def listar_partidos_torneo(torneo_id):
	try:
		partidos = partido_service.get_by_torneo(torneo_id)
		return jsonify(partidos_schema.dump(partidos))
	except Exception as e:
		return jsonify({"error": str(e)}), 500

# Registrar resultado de un partido
@bp_partido.patch('/<int:id>/resultado')
def registrar_resultado(id):
	data = request.get_json()
	try:
		partido = partido_service.registrar_resultado(id, data)
		return jsonify(partido_schema.dump(partido)), 200
	except ValueError as e:
		return jsonify({"error": str(e)}), 400
	except Exception as e:
		return jsonify({"error": "Error al registrar el resultado del partido" + str(e)}), 500

