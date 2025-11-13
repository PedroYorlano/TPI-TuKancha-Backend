from flask import Blueprint, jsonify, request
from app import db
from app.services.reserva_service import ReservaService
from app.schemas.reserva_schema import reserva_schema, reservas_schema

bp_reserva = Blueprint("reserva", __name__, url_prefix="/api/v1/reservas")

reserva_service = ReservaService()

# Obtener todas las reservas
@bp_reserva.get("/")
def get_all():
    reservas = reserva_service.get_all()
    return reservas_schema.dump(reservas)

# Obtener una reserva por su ID
@bp_reserva.get("/<int:id>")
def get_by_id(id):
    reserva = reserva_service.get_by_id(id)
    return reserva_schema.dump(reserva)

# Crear una nueva reserva
@bp_reserva.post("/")
def create():
    data = request.json
    try:
        reserva = reserva_service.create(data)
        return jsonify(reserva_schema.dump(reserva)), 201
    except ValueError as e:
        # Errores de validación (timeslot no disponible, campos faltantes, etc.)
        print(f"Error de validación al crear reserva: {str(e)}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        # Errores inesperados
        import traceback
        print("=" * 50)
        print("ERROR AL CREAR RESERVA:")
        print(f"Tipo: {type(e).__name__}")
        print(f"Mensaje: {str(e)}")
        traceback.print_exc()
        print("=" * 50)
        return jsonify({"error": "Error al crear la reserva", "details": str(e)}), 500

# Eliminar una reserva
@bp_reserva.delete("/<int:id>")
def delete(id):
    try:
        reserva_service.delete(id)
        return jsonify({"message": "Reserva eliminada exitosamente"}), 200
    except ValueError as e:
        # Errores de validación (reserva no encontrada, etc.)
        print(f"Error de validación al eliminar reserva: {str(e)}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        # Errores inesperados
        import traceback
        print("=" * 50)
        print("ERROR AL ELIMINAR RESERVA:")
        print(f"Tipo: {type(e).__name__}")
        print(f"Mensaje: {str(e)}")
        traceback.print_exc()
        print("=" * 50)
        return jsonify({"error": "Error al eliminar la reserva", "details": str(e)}), 500


